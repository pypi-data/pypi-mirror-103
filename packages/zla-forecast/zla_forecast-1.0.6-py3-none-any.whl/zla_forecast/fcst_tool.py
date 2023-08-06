from zla_material_class.zla_class import ws_class
from zla_backend.forecasting import series_fbprophet as fb

def _get_fcst_graph(_partno,_start=None,_end=None):
    _x = ws_class.get_ws(partno=_partno,start=_start,end=_end).new_deldata
    _x['del1stdate'] = _x['del1stdate'].astype('datetime64[ns]')
    _y = _x.groupby('del1stdate').sum()['qty']
    _fcst, _model, _backfcst, _matrix, _rowdata, _fig =  fb.fcst_series_fbprophet(_raw=_y,_freq='months',forward=12,backward =4)
    return _fcst,_fig