import pandas as pd
import numpy as np

# List of your feature columns
columns = ['duration', 'orig_bytes', 'resp_bytes', 'missed_bytes', 'orig_pkts', 'orig_ip_bytes',
           'resp_pkts', 'resp_ip_bytes', 'proto_icmp', 'proto_tcp', 'proto_udp',
           'conn_state_OTH', 'conn_state_REJ', 'conn_state_RSTO', 'conn_state_RSTOS0',
           'conn_state_RSTR', 'conn_state_RSTRH', 'conn_state_S0', 'conn_state_S1',
           'conn_state_S2', 'conn_state_S3', 'conn_state_SF', 'conn_state_SH', 'conn_state_SHR']

# Generate 5 rows of random data
data = []

for _ in range(5):
    row = [
        np.random.uniform(0, 1000),  # duration
        np.random.randint(0, 100000),  # orig_bytes
        np.random.randint(0, 100000),  # resp_bytes
        np.random.randint(0, 1000),    # missed_bytes
        np.random.randint(0, 100),     # orig_pkts
        np.random.randint(0, 100000),  # orig_ip_bytes
        np.random.randint(0, 100),     # resp_pkts
        np.random.randint(0, 100000),  # resp_ip_bytes
        np.random.randint(0, 2),       # proto_icmp (binary)
        np.random.randint(0, 2),       # proto_tcp
        np.random.randint(0, 2),       # proto_udp
        np.random.randint(0, 2),       # conn_state_OTH
        np.random.randint(0, 2),       # conn_state_REJ
        np.random.randint(0, 2),       # conn_state_RSTO
        np.random.randint(0, 2),       # conn_state_RSTOS0
        np.random.randint(0, 2),       # conn_state_RSTR
        np.random.randint(0, 2),       # conn_state_RSTRH
        np.random.randint(0, 2),       # conn_state_S0
        np.random.randint(0, 2),       # conn_state_S1
        np.random.randint(0, 2),       # conn_state_S2
        np.random.randint(0, 2),       # conn_state_S3
        np.random.randint(0, 2),       # conn_state_SF
        np.random.randint(0, 2),       # conn_state_SH
        np.random.randint(0, 2)        # conn_state_SHR
    ]
    data.append(row)

# Create DataFrame and save to CSV
df = pd.DataFrame(data, columns=columns)
df.to_csv("random_ids_data.csv", index=False)

print("random_ids_data.csv created successfully.")
