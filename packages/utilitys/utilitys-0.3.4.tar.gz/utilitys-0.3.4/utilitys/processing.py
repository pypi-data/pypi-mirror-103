from __future__ import annotations

import copy as _copy
import inspect
import typing as t
from abc import ABC, abstractmethod
from functools import wraps
from warnings import warn

import numpy as np
from pyqtgraph.Qt import QtCore

from .fns import nameFormatter

__all__ = ['ProcessIO', 'ProcessStage', 'NestedProcess', 'AtomicProcess']

_infoType = t.List[t.Union[t.List, t.Dict[str, t.Any]]]
StrList = t.List[str]
StrCol = t.Collection[str]

class ProcessIO(dict):
  """
  The object through which the processor pipeline communicates data. Inputs to one process
  become updated by the results from that process, and this updated ProcessIO is used
  as the input to the *next* process.
  """

  class FROM_PREV_IO:
    """
    Helper class to indicate whether a key in this IO is supposed to come from
    a previous process stage. Typical usage:
    ```if not hyperparam: self[k] = self.FROM_PREV_IO```

    Typically, process objects will have two IO dictionaries: One that hold the input spec
    (which makes use of `FROM_PREV_IO`) and one that holds the runtime process values. The
    latter IO will not make use of `FROM_PREV_IO`.
    """

  def __init__(self, hyperParamKeys: t.Sequence[str]=None, **kwargs) -> None:
    """
    :param hyperParamKeys: Hyperparameters for this process that aren't expected to come
      from the previous stage in the process. Forwarded keys (that were passed from a
      previous stage) are inferred by everything that is not a hyperparameter key.
    :param kwargs: see *dict* init
    """
    if hyperParamKeys is None:
      hyperParamKeys = []
    self.hyperParamKeys = hyperParamKeys
    warnKeys = []
    for k in self.hyperParamKeys:
      if k not in kwargs:
        warnKeys.append(k)
        kwargs[k] = None
    if warnKeys:
      warn(f'Hyperparameter keys were specified, but did not exist in provided'
           f' inputs:\n{warnKeys}\n'
           f'Defaulting to `None` for those keys.', UserWarning)
    super().__init__(**kwargs)
    self.keysFromPrevIO = set(self.keys()) - set(self.hyperParamKeys)

  @classmethod
  def fromFunction(cls, func: t.Callable, ignoreKeys: StrCol=None, **overriddenDefaults):
    """
    In the ProcessIO scheme, default arguments in a function signature constitute algorithm
    hyperparameters, while required arguments must be provided each time the function is
    run. If `**overriddenDefaults` is given, this will override any default arguments from
    `func`'s signature.
    :param func: Function whose input signature should be parsed
    :param ignoreKeys: Keys to disregard entirely from the incoming function. This is useful for cases like adding
      a function at the class instead of instance level and `self` shouldn't be regarded by the parser.
    :param overriddenDefaults: Keys here that match default argument names in `func` will
      override those defaults. If an argument does _not_ have a default in the function definition but should
      be shown to the user, provide a default here and it will appear.
    """
    if ignoreKeys is None:
      ignoreKeys = []
    outDict = {}
    hyperParamKeys = []
    spec = inspect.signature(func).parameters
    for k, v in spec.items():
      if (k in ignoreKeys
              or v.kind in (v.VAR_POSITIONAL, v.VAR_KEYWORD)):
        continue
      formattedV = overriddenDefaults.get(k, v.default)
      if formattedV is v.empty:
        formattedV = cls.FROM_PREV_IO
        # Not a hyperparameter
      else:
        hyperParamKeys.append(k)
      outDict[k] = formattedV
    # Make sure to avoid 'init got multiple values' error
    initSig = inspect.signature(cls.__init__).parameters
    keys = list(outDict)
    for key in keys:
      if key in initSig:
        newName = '_' + key
        outDict[newName] = outDict[key]
        del outDict[key]
    return cls(hyperParamKeys, **outDict)

class ProcessStage(ABC):
  name: str
  input: ProcessIO = None
  allowDisable = False
  disabled = False
  cacheOnDisable = False
  result: ProcessIO = None
  mainResultKeys: StrList = None
  mainInputKeys: StrList = None

  class _DUPLICATE_INFO: pass
  """Identifies information that is the same in two contiguous stages"""

  def __repr__(self) -> str:
    selfCls = type(self)
    oldName: str = super().__repr__()
    # Remove module name for brevity
    oldName = oldName.replace(f'{selfCls.__module__}.{selfCls.__name__}',
                              f'{selfCls.__name__} \'{self.name}\'')
    return oldName

  def __str__(self) -> str:
    return repr(self)

  def __eq__(self, other: NestedProcess):
    return self.saveState(True, True) == other.saveState(True, True)

  def __hash__(self):
    return id(self)

  def updateInput(self, prevIo: ProcessIO=None, graceful=False, **kwargs):
    """
    Helper function to update current inputs from previous ones while ignoring leading
    underscores.

    :param prevIo: Io object to forward updated inputs here. Extra inputs can be supplied to **kwargs
    :param graceful: If *True*, doesn't error on missing keys or bad update hierarchy
    """
    if prevIo is None:
      prevIo = ProcessIO()
    useIo = prevIo.copy()
    useIo.update(kwargs)
    selfFmtToUnfmt = {k.lstrip('_'): k for k in self.input}
    requiredKeyFmt = {k: v for k, v in selfFmtToUnfmt.items() if v in self.input.keysFromPrevIO}
    prevIoKeyToFmt = {k.lstrip('_'): k for k in {**useIo}}
    missingKeys = []
    for fmtK, trueK in selfFmtToUnfmt.items():
      if fmtK in prevIoKeyToFmt:
        self.input[trueK] = useIo[prevIoKeyToFmt[fmtK]]
      elif fmtK in requiredKeyFmt:
        missingKeys.append(fmtK)
    if missingKeys and not graceful:
      raise KeyError(f'Missing Following keys from {self}: {missingKeys}')

  def run(self, io: ProcessIO=None, disable=False, **runKwargs):
    raise NotImplementedError

  def __call__(self, **kwargs):
    return self.run(ProcessIO(**kwargs))

  def __iter__(self):
    raise NotImplementedError

  def saveState(self, includeDefaults=False, includeMeta=False):
    """
    Serializes the process' state in terms of its composition and inputs.

    :param includeDefaults: Whether to also serialize inputs that are unchanged from the original process creation
    :param includeMeta: Whether to also serialize metadata about the stage such as its disable/allowDisable status
    """
    raise NotImplementedError

  def saveState_flattened(self, includeDefault=False, includeMeta=False):
    """Saves state while collapsing all nested processes into one list of atomic processes"""
    return self.saveState(includeDefault, includeMeta)

  def saveMetaProps(self, **filterOpts):
    """
    Converts a saved state of parameters and staegs to one including disabled and allowDisable statuses

    :param filterOpts: Values to ignore if they match. So, passing `disabled=True` will only
      record the `disabled` property if it is *False*. This is an easy way of ignoring default properties. Setting a key
      to *None* will ignore that property entirely.
    """
    metaProps = ('allowDisable', 'disabled')
    # Convert back if no props were added
    out = {}
    for k in metaProps:
      selfVal = getattr(self, k)
      cmp = filterOpts.get(k)
      if cmp is None or np.array_equal(cmp, selfVal):
        continue
      out[k] = selfVal
    return out

  def addMetaProps(self, state: t.Union[dict, str], **metaFilterOpts):
    """
    Helper method to insert meta properties into the current state. Since the state might be a string, or meta props
    might be empty, this performs checks to ensure only the most simplified output form is preserved
    """
    state = _copy.copy(state)
    metaProps = self.saveMetaProps(**metaFilterOpts)
    if not metaProps:
      return state
    if isinstance(state, str):
      state = {state: {}}
    state.update(metaProps)
    return state

class AtomicProcess(ProcessStage):
  """
  Often, process functions return a single argument (e.g. string of text,
  processed image, etc.). In these cases, it is beneficial to know what name should
  be assigned to that result.
  """

  def __init__(self, func: t.Callable, name:str=None, *, needsWrap=False,
               mainResultKeys: StrList=None, mainInputKeys: StrList=None,
               **procIoKwargs):
    """
    :param func: Function to wrap
    :param name: Name of this process. If `None`, defaults to the function name with
      camel case or underscores converted to title case.
    :param needsWrap: For functions not defined by the user, it is often inconvenient if they have
    to be redefined just to return a FRProcessIO object. If `func` does not return a `FRProcessIO`
    object, `needsWrap` can be set to `True`. In this case, `func` is assumed to
    returns either one result or a list of results. It is converted into a function
    returning a FRProcessIO object instead. Each `mainResultKey` is assigned to each output
    of the function in order. If only one main result key exists, then the output of the
    function is assumed to be that key. I.e. in the case where `len(cls.mainResultKeys) == 1`,
    the output is expected to be the direct result, not a sequence of results per key.
    :param mainResultKeys: Set by parent process as needed
    :param mainInputKeys: Set by parent process as needed
    :param procIoKwargs: Passed to ProcessIO.fromFunction
    """
    if name is None:
      name = nameFormatter(func.__name__)
    if mainResultKeys is not None:
      self.mainResultKeys = mainResultKeys
    if mainInputKeys is not None:
      self.mainInputKeys = mainInputKeys

    self.name = name
    self.input = ProcessIO.fromFunction(func, **procIoKwargs)
    self.result: t.Optional[ProcessIO] = None

    if mainInputKeys is not None:
      keys = set(self.input.keys())
      missingKeys = set(mainInputKeys) - keys
      if missingKeys:
        raise KeyError(f'{name} input signature is missing the following required input keys:\n'
                                f'{missingKeys}')

    if needsWrap:
      func = self._wrappedFunc(func, self.mainResultKeys)
    self.func = func
    self.defaultInput = self.input.copy()

  @classmethod
  def _wrappedFunc(cls, func, mainResultKeys: StrList=None):
    """
    Wraps a function returining either a result or list of results, instead making the
    return value an `FRProcessIO` object where each `cls.mainResultkey` corresponds
    to a returned value
    """
    if mainResultKeys is None:
      mainResultKeys = cls.mainResultKeys
    if len(mainResultKeys) == 1:
      @wraps(func)
      def newFunc(*args, **kwargs):
        return ProcessIO(**{mainResultKeys[0]: func(*args, **kwargs)})
    else:
      @wraps(func)
      def newFunc(*args, **kwargs):
        return ProcessIO(**{k: val for k, val in zip(mainResultKeys, func(*args, **kwargs))})
    return newFunc

  @property
  def keysFromPrevIO(self):
    return self.input.keysFromPrevIO

  def run(self, io: ProcessIO=None, disable=False, **runKwargs):
    ProcessIO.count = self
    disable = disable or self.disabled
    self.updateInput(io, **runKwargs)
    if not disable:
      self.result = self.func(**self.input)
    elif not self.cacheOnDisable:
      self.result = None
    out = self.result
    if out is None:
      out = self.input
    return out

  def saveState(self, includeDefaults=False, includeMeta=False, **metaFilterOpts):
    def keepCond(k, v):
      return (k in self.input.hyperParamKeys or k not in self.defaultInput) \
              and (includeDefaults or v != self.defaultInput.get(k)) \
              and v is not self.input.FROM_PREV_IO
    saveIo = {k: v for k, v in self.input.items() if keepCond(k, v)}
    if not saveIo:
      state = self.name
    else:
      state = {self.name: saveIo}
    if includeMeta:
      state = self.addMetaProps(state, **metaFilterOpts)
    return state

  def __iter__(self):
    return iter([])

class NestedProcess(ProcessStage):

  def __init__(self, name: str=None, mainInputKeys: StrList=None, mainResultKeys: StrList=None):
    self.stages: t.List[ProcessStage] = []
    self.name = name
    self.allowDisable = True
    self.result = ProcessIO()
    if mainInputKeys is not None:
      self.mainInputKeys = mainInputKeys
    if mainResultKeys is not None:
      self.mainResultKeys = mainResultKeys

  def addFunction(self, func: t.Callable, keySpec: t.Union[t.Type[NestedProcess], NestedProcess]=None, **kwargs):
    """
    Wraps the provided function in an AtomicProcess and adds it to the current process.
    :param func: Forwarded to AtomicProcess
    :param kwargs: Forwarded to AtomicProcess
    :param keySpec: This argument should have 'mainInputKeys' and 'mainResultKeys' that are used
      when adding a function to this process. This can be beneficial when an Atomic Process
      is added with different keys than the current process type
    """
    if keySpec is None:
      keySpec = self
    atomic = AtomicProcess(func, mainResultKeys=keySpec.mainResultKeys, mainInputKeys=keySpec.mainInputKeys, **kwargs)
    numSameNames = sum(
        atomic.name == stage.name.split('#')[0] for stage in self)
    if numSameNames > 0:
      atomic.name = f'{atomic.name}#{numSameNames+1}'
    if self.name is None:
      self.name = atomic.name
    self.stages.append(atomic)
    return atomic

  @classmethod
  def fromFunction(cls, func: t.Callable, **kwargs):
    name = kwargs.get('name', None)
    out = cls(name)
    out.addFunction(func, **kwargs)
    return out

  def addProcess(self, process: ProcessStage):
    if self.name is None:
      self.name = process.name
    self.stages.append(process)
    return process

  def updateInput(self, prevIo: ProcessIO=None, graceful=False, **kwargs):
    """Drill down to the necessary stages when setting input values when setter values are dicts"""
    if prevIo is None:
      prevIo = ProcessIO()
    prevIo.update(kwargs)
    for kk in list(prevIo):
      # List wrap instead of items() to avoid mutate error
      vv = prevIo[kk]
      if isinstance(vv, dict):
        matchStage = [s for s in self if s.name == kk]
        if not matchStage and not graceful:
          raise ValueError(f'Name {kk} doesn\'t match existing stages')
        elif not matchStage:
          continue
        matchStage[0].updateInput(**vv, graceful=graceful)
        prevIo.pop(kk)
    # Normal input maps to first stage, so propagate all normal args there
    self.stages[0].updateInput(prevIo, graceful=graceful)

  def run(self, io: ProcessIO = None, disable=False, **runKwargs):
    _activeIo = ProcessIO() if not io else _copy.copy(io)
    _activeIo.update(runKwargs)

    if self.disabled or disable and not self.result:
      # TODO: Formalize this behavior. Disabling before being run should avoid eating the input args
      return _activeIo

    for i, stage in enumerate(self):
      newIo = stage.run(_activeIo, disable=disable or self.disabled)
      if not isinstance(newIo, ProcessIO) and isinstance(stage, AtomicProcess):
        # Try wrapping the inner function for future runs
        newIo = self._maybeWrapStageFunc(stage, newIo)
      if isinstance(newIo, ProcessIO):
        _activeIo.update(newIo)

    self.result = _activeIo
    return self.result

  def _maybeWrapStageFunc(self, stage: AtomicProcess, oldresult: t.Any):
    oldFunc = stage.func
    useKeys = stage.mainResultKeys or self.mainResultKeys
    try:
      stage.func = stage._wrappedFunc(oldFunc, useKeys)
      # Capture current result as a process io
      def dummyFunc():
        return oldresult
      oldresult = stage._wrappedFunc(dummyFunc, useKeys)()
    except Exception:
      stage.func = oldFunc
    return oldresult

  def saveState(self, includeDefaults=False, includeMeta=False, **metaFilterOpts):
    stageStates = []
    for stage in self:
      curState = stage.saveState(includeDefaults, includeMeta)
      stageStates.append(curState)
    state = {self.name: stageStates}
    if includeMeta:
      state = self.addMetaProps(state, **metaFilterOpts)
    return state

  def saveState_flattened(self, **kwargs):
    """Saves state while collapsing all nested processes into one list of atomic processes"""
    return self.flatten().saveState(**kwargs)

  @property
  def input(self):
    return self.stages[0].input

  def flatten(self, copy=True, includeDisabled=True):
    if copy:
      outProc = type(self)(self.name, self.mainInputKeys, self.mainResultKeys)
    else:
      outProc = self
    outProc.stages = self._getFlatStages(includeDisabled)
    return outProc

  @property
  def stages_flattened(self):
    """Property version of flattened self which, like `stages`, will always include disabled stages"""
    return self._getFlatStages()

  def _getFlatStages(self, includeDisabled=True):
    outStages: t.List[ProcessStage] = []
    for stage in self:
      if stage.disabled and not includeDisabled:
        continue
      if isinstance(stage, AtomicProcess):
        outStages.append(stage)
      else:
        stage: NestedProcess
        outStages.extend(stage._getFlatStages(includeDisabled))
    return outStages

  def __iter__(self):
    return iter(self.stages)

  def _stageSummaryWidget(self):
    raise NotImplementedError

  def _nonDisabledStages_flattened(self):
    out = []
    for stage in self:
      if isinstance(stage, AtomicProcess):
        out.append(stage)
      elif not stage.disabled:
        stage: NestedProcess
        out.extend(stage._nonDisabledStages_flattened())
    return out

  def stageSummary_gui(self):
    if self.result is None:
      raise RuntimeError('Analytics can only be shown after the algorithm was run.')
    outGrid = self._stageSummaryWidget()
    outGrid.showMaximized()
    def fixedShow():
      for item in outGrid.ci.items:
        item.getViewBox().autoRange()
    QtCore.QTimer.singleShot(0, fixedShow)

  def getStageInfos(self, ignoreDuplicates=True):
    allInfos: _infoType = []
    lastInfos = []
    for stage in self._nonDisabledStages_flattened():
      res = stage.result
      if not isinstance(res, ProcessIO): continue
      if any(k not in res for k in self.mainResultKeys):
        # Missing required keys, not sure how to turn into summary info. Skip
        continue
      if 'summaryInfo' not in res:
        defaultSummaryInfo = {k: res[k] for k in self.mainResultKeys}
        defaultSummaryInfo.update(name=stage.name)
        res['summaryInfo'] = defaultSummaryInfo
      if res['summaryInfo'] is None:
        continue
      infos = stage.result['summaryInfo']
      if not isinstance(infos, t.Sequence):
        infos = [infos]
      if not ignoreDuplicates:
        validInfos = infos
      else:
        validInfos = self._cmpPrevCurInfos(lastInfos, infos)
      lastInfos = infos
      for info in validInfos:
        stageNameCount = 0
        if info.get('name', None) is None:
          newName = stage.name
          if stageNameCount > 0:
            newName = f'{newName}#{stageNameCount}'
          info['name'] = newName
        stageNameCount += 1
      allInfos.extend(validInfos)
    return allInfos

  @classmethod
  def _cmpPrevCurInfos(cls, prevInfos: t.List[dict], infos: t.List[dict]):
    """
    This comparison allows keys from the last result which exactly match keyts from the
    current result to be discarded for brevity.
    """
    validInfos = []
    for info in infos:
      validInfo = _copy.copy(info)
      for lastInfo in prevInfos:
        for key in set(info.keys()).intersection(lastInfo.keys()) - {'name'}:
          if np.array_equal(info[key], lastInfo[key]):
            validInfo[key] = cls._DUPLICATE_INFO
      validInfos.append(validInfo)
    return validInfos