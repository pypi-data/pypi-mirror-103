from time import sleep
from epics import caget
from . import caput

def writeChannels(chanInfo):
    '''
    Write epics channels given in a dictionary format together.
    '''
    kwargs = {}
    for ch in chanInfo['channels']:
        for arg in ['wait', 'timeout']:
            kwargs[ch] = {}
            if arg in chanInfo:  # If present as global argument
                kwargs[ch][arg] = chanInfo[arg]
            elif arg in chanInfo['channels'][ch]:
                kwargs[ch][arg] = chanInfo['channels'][ch][arg]
    try:
        rampYourself = True
        if 'tramp' in chanInfo:
            oldTramps = {}
            if chanInfo['tramp'] > 0:
                for ch in chanInfo['channels']:
                    fus = ch.rfind('_') + 1
                    if ch[fus:] in ['GAIN', 'OFFSET']:
                        try:
                            trampCh = ch[:fus] + 'TRAMP'
                            oldTramps[trampCh] = caget(trampCh)
                            rampYourself = rampYourself and False
                        except BaseException:
                            rampYourself = rampYourself or True
                    else:
                        rampYourself = rampYourself or True
                if rampYourself:
                    for ch in oldTramps:
                        caput(ch, 0)
                    rampSteps = 100
                    sleepTime = chanInfo['tramp'] / rampSteps
                    curVals = {}
                    for ch in chanInfo['channels']:
                        curVals[ch] = caget(ch)
                    stepVals = {}
                    for ch in curVals:
                        stepVals[ch] = (chanInfo['channels'][ch]['value']
                                        - curVals[ch]) / rampSteps
                    for tstep in range(1, rampSteps):
                        sleep(sleepTime)
                        for ch in chanInfo['channels']:
                            caput(ch, curVals[ch] + tstep * stepVals[ch],
                                  **kwargs[ch])
                else:
                    for ch in oldTramps:
                        caput(ch, chanInfo['tramp'])
            # Write final values
            for ch in chanInfo['channels']:
                caput(ch, chanInfo['channels'][ch]['value'], **kwargs[ch])
            if not rampYourself:
                sleep(chanInfo['tramp'])
            sleep(0.1)  # Buffer time
            for ch in oldTramps:
                caput(ch, oldTramps[ch])
        else:
            for ch in chanInfo['channels']:
                if 'tramp' in chanInfo['channels'][ch]:
                    kwargs[ch]['tramp'] = chanInfo['channels'][ch]['tramp']
                caput(ch, chanInfo['channels'][ch]['value'], **kwargs[ch])
    except BaseException:
        restoreEpics()
        traceback.print_exc()
