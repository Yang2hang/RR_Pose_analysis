from scipy.interpolate import make_interp_spline
import pandas as pd
from os.path import join as oj
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

class PoseSeries:

    """PoseSeries organizes processed track files and compile them into a long form time series.
    Importantly, PoseSeries may contain a temporally disjoint set of poses, with each pose sequence
    refer to a predefined motion series aligned to tone onsets.

    Input:
        root: root directory for track files
        animal: animal id
        session: session id
    
    Key Attributes:
        track_df: tracks from sleap, with raw keypoints coordinate tracks
        sleap_tdf: trial structure based dataframe with sleap-labeled events
    """

    def __init__(self, root, animal, session):
        track_session_root = oj(root, animal, session)
        tracks = []
        for r in range(1, 5):
            track_f = oj(track_session_root, f'{animal}_{session}_R{r}_tracks_processed.csv')
            tdf = pd.read_csv(track_f)
            tdf['restaurant'] = r
            tdf['restaurant'] = tdf['restaurant'].astype(int)
            tdf['trial'] = tdf['trial'].astype(int)
            tdf.rename(columns={'decision': 'sleap_event'}, inplace=True)
            tdf['sleap_event'].replace('T-Entry', 'T_Entry', inplace=True)
            tracks.append(tdf)
        track_df = pd.concat(tracks, axis=0, ignore_index=True)
        self.track_df = track_df
        self.sleap_tdf = self.summarize_sleap_info()
        self.sleap_tdf['animal'] = animal
        self.sleap_tdf['session'] = session
        self.track_df['animal'] = animal
        self.track_df['session'] = session
        self.animal = animal
        self.session = session
    
    def summarize_sleap_info(self):
        track_df = self.track_df
        sleap_tdf = track_df.loc[track_df['sleap_event']=='T_Entry', ['trial', 'time', 'rel_time', 'sleap_event', 'restaurant']].sort_values(['trial', 'rel_time']).reset_index(drop=True)
        sleap_tdf.rename(columns={'time': 'slp_T_Entry_time', 'rel_time': 'slp_hall_time'}, inplace=True)
        sleap_tdf['slp_tone_onset_time'] = sleap_tdf['slp_T_Entry_time'] - sleap_tdf['slp_hall_time']
        dfa = track_df.loc[track_df['sleap_event']=='ACC', ['trial', 'time', 'rel_time', 'sleap_event']].sort_values(['trial', 'rel_time'])
        dfb = track_df.loc[track_df['sleap_event']=='REJ', ['trial', 'time', 'rel_time', 'sleap_event']].sort_values(['trial', 'rel_time'])
        dfc = pd.concat([dfa, dfb], axis=0, ignore_index=True)
        dfc.rename(columns={'time': 'slp_choice_time'}, inplace=True)
        dfc['slp_accept'] = dfc['sleap_event'].map({'ACC': 1, 'REJ': 0})
        dfc.drop(columns=['sleap_event', 'rel_time'], inplace=True)
        sleap_tdf = pd.merge(sleap_tdf, dfc, on='trial', how='left')
        dfd = track_df.loc[track_df['sleap_event']=='quit', ['trial', 'time', 'rel_time']].sort_values(['trial', 'rel_time']).reset_index(drop=True)
        dfd.rename(columns={'time': 'slp_quit_time'}, inplace=True)
        sleap_tdf = pd.merge(sleap_tdf, dfd[['trial', 'slp_quit_time']], on='trial', how='left')
        sleap_tdf.drop(columns=['sleap_event'], inplace=True)
        dur_df = track_df.groupby('trial', as_index=False).agg({'rel_time': 'max'})
        dur_df.rename(columns={'rel_time': 'duration'}, inplace=True)
        sleap_tdf = sleap_tdf.merge(dur_df, how='left', on='trial')
        sleap_tdf['slp_decision'] = sleap_tdf['slp_accept'].astype(float).map({1.0: 'accept', 0.0: 'reject'})
        sleap_tdf.loc[~sleap_tdf['slp_quit_time'].isnull(), 'slp_decision'] = 'quit'
        return sleap_tdf
    
    def preprocess_track_df(self, resample_interval=0.05):
        # resample, calculate velocity and angular velocity
        def resamp_track_df_calc_v(tdf, meas_cols, resample_interval=0.05):
            t0 = tdf['time'].values[0]
            max_time = tdf['rel_time'].values[-1]
            x = tdf['rel_time'].values
            xnew = np.arange(0, max_time+1e-5, resample_interval)
            new_df = pd.DataFrame({'time': xnew+t0, 'rel_time': xnew})
            for i in range(len(meas_cols)):
                # ONLY interpolation, no extrapolation
                y = tdf[meas_cols[i]].values
                bspl = make_interp_spline(x, y, k=3)
                der = bspl.derivative() # 1st derivative
                ynew = bspl(xnew)
                parts = meas_cols[i].split(' ')
                pream = '_'.join(parts[:-1])
                new_df['_'.join(parts)] = ynew
                # new_df[f'{kp}_wv{coord}'] = der(xnew) # using bspline derivative
                new_df[f'{pream}_vel_{parts[-1]}'] = np.gradient(ynew) *1/resample_interval # using bspline derivative
            return new_df
        
        track_df = self.track_df
        pre_tdf = track_df[['trial', 'time', 'rel_time'] + list(track_df.columns[8:16])].reset_index(drop=True)
        resamp_track_df = pre_tdf.groupby('trial', as_index=True).apply(resamp_track_df_calc_v, 
                                                                        meas_cols=track_df.columns[8:16], resample_interval=resample_interval).reset_index()
        resamp_track_df.drop(columns=['level_1'], inplace=True)
        resamp_track_df['animal'] = self.animal
        resamp_track_df['session'] = self.session
        return resamp_track_df
    
class PlotlyFig:
    # TODO: add automatic color palette

    def __init__(
        self, rows=1, cols=1, shared_xaxes=True, vertical_spacing=0.1, **kwargs
    ):
        fig = make_subplots(
            rows=rows,
            cols=cols,
            shared_xaxes=shared_xaxes,
            vertical_spacing=vertical_spacing,
            **kwargs,
        )
        self.fig = fig

    def plot(
        self, x, y, name="", color="blue", mode="lines+markers", row=1, col=1, **kwargs
    ):
        self.fig.add_trace(
            go.Scatter(x=x, y=y, mode=mode, name=name, line=dict(color=color)),
            row=row,
            col=col,
        )

    def show(self):
        self.fig.show()