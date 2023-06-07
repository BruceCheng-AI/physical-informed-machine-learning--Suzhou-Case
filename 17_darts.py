import pandas as pd
from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler
from darts.metrics import rmse
import torch
from darts.models import BlockRNNModel


# load data
history = pd.read_csv('../data/results/history.csv', index_col=0)
ssp245 = pd.read_csv('../data/results/ssp245.csv', index_col=0)
ssp585 = pd.read_csv('../data/results/ssp585.csv', index_col=0)
history_wl = pd.read_csv('../data/results/history_wl.csv', index_col=0)

# 从数据框创建时间序列
series_history = TimeSeries.from_dataframe(history.reset_index(), 'time')
series_wl = TimeSeries.from_dataframe(history_wl.reset_index(), 'time', ['water_level'])



# 数据预处理
scaler_history = Scaler()
scaler_wl = Scaler()

series_history_scaled = scaler_history.fit_transform(series_history)
series_wl_scaled = scaler_wl.fit_transform(series_wl)

# Determine the split point
split_idx = int(len(series_wl_scaled) * 0.8)
split_date = series_wl_scaled.time_index[split_idx]

# split data into training and validation sets
wl_train = series_wl_scaled.split_before(split_date)
wl_val = series_wl_scaled.split_after(split_date)

covariates_history_train = series_history_scaled.split_before(split_date)
covariates_history_val = series_history_scaled.split_after(split_date)



torch.set_float32_matmul_precision('medium')
model = BlockRNNModel(
    model='LSTM', 
    input_chunk_length=30, 
    output_chunk_length=10,
    n_rnn_layers=2,
    random_state=42,
    pl_trainer_kwargs = {"accelerator": "gpu", "devices": [0]}  
)

model.fit(
    series=wl_train,
    past_covariates=covariates_history_train,
    verbose=True,
    epochs=10
)


# 使用模型进行预测
prediction = model.predict(n=len(wl_val), series=wl_val, past_covariates=covariates_history_val)



# 计算 RMSE
error = rmse(prediction, wl_val)

print(f'RMSE: {error}')

# save model
model.save_model('model.pkl')

