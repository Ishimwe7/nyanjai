import pandas as pd
from timezonefinder import TimezoneFinder
import pytz

def apply_qc_checks(df):
    # """
    # 1. Channel A/B validation (>70% difference check)
    # 2. Physical Implausibility (Humidity > 100)
    # 3. Stuck sensor check (12h zero variation in BOTH PM and Temp)
    # """
    # # 1. Channel AB Check
    # # Note: PurpleAir API uses 'pm2.5_cf_1' (A) and 'pm2.5_cf_1_b' (B)
    # if 'pm2.5_cf_1' in df.columns and 'pm2.5_cf_1_b' in df.columns:
    #     avg_pm = (df['pm2.5_cf_1'] + df['pm2.5_cf_1_b']) / 2
    #     diff = abs(df['pm2.5_cf_1'] - df['pm2.5_cf_1_b']) / avg_pm
    #     # Keep if diff <= 70% OR if one channel is missing (per rubric)
    #     df = df[(diff <= 0.70) | (df['pm2.5_cf_1_b'].isna())]

    # # 2. Physical Implausibility
    # df = df[df['humidity'] <= 100]

    # Logic to handle the 'one channel vs two channels' exception
    if 'pm2.5_cf_1' in df.columns and 'pm2.5_cf_1_b' in df.columns:
        # Calculate relative difference only where both exist
        mask_both = df['pm2.5_cf_1'].notna() & df['pm2.5_cf_1_b'].notna()
        
        avg_pm = (df['pm2.5_cf_1'] + df['pm2.5_cf_1_b']) / 2
        diff = abs(df['pm2.5_cf_1'] - df['pm2.5_cf_1_b']) / avg_pm
        
        # Discard only if both are present AND they disagree > 70%
        to_discard = mask_both & (diff > 0.70)
        df = df[~to_discard]
    
    # Other checks (Physical implausibility & Stuck sensors)
    df = df[df['humidity'] <= 100] # [cite: 72]
        
    # 3. Stuck sensor check (12 consecutive hours of ZERO variance in both)
    # This must be done per sensor
    def remove_stuck(group):
        # Calculate rolling standard deviation over 12 samples (12 hours)
        pm_std = group['pm2.5_cf_1'].rolling(window=12).std()
        temp_std = group['temperature'].rolling(window=12).std()
        
        # Identify rows where BOTH have 0 variance
        stuck_mask = (pm_std == 0) & (temp_std == 0)
        return group[~stuck_mask]

    df = df.groupby('sensor_index', group_keys=False).apply(remove_stuck)
    return df

def convert_to_local_time(df):
    """Requirement: Convert UTC to Local time based on Lat/Lon"""
    tf = TimezoneFinder()
    lat, lon = df['latitude'].iloc[0], df['longitude'].iloc[0]
    tz_str = tf.timezone_at(lng=lon, lat=lat)
    local_tz = pytz.timezone(tz_str)
    
    df['time_stamp'] = pd.to_datetime(df['time_stamp'], unit='s', utc=True)
    df['local_time'] = df['time_stamp'].dt.tz_convert(local_tz)
    return df

def barkjohn_correction(pm_raw, humidity):
    if pm_raw > 250:
        return pm_raw 
    return (0.524 * pm_raw) - (0.0862 * humidity) + 5.75