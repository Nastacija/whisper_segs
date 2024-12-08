from itertools import product

letters = "GBRY"
nums = "1234"
levels = [ch + num for num, ch in product(nums, letters)]
level_codes = [2 ** i for i in range(len(levels))]
code_to_level = {i: j for i, j in zip(level_codes, levels)}
level_to_code = {j: i for i, j in zip(level_codes, levels)}

def write_seg(s_freq, bps, n_ch, labels, filename, encoding = "utf-8-sig"):
    param_defaults = {
        "SAMPLING_FREQ": s_freq,
        "BYTE_PER_SAMPLE": bps,
        "CODE": 0,
        "N_CHANNEL": n_ch,
        "N_LABEL": 0
    }
    param_defaults["N_LABEL"] = len(labels)
    with open(filename, "w", encoding=encoding) as f:
        f.write("[PARAMETERS]\n")
        for key, value in param_defaults.items():
            f.write(f"{key}={value}\n")
        f.write("[LABELS]\n")
        for label in labels:
            f.write(f"{param_defaults['BYTE_PER_SAMPLE'] * param_defaults['N_CHANNEL'] * label['position']},")
            f.write(f"{level_to_code[label['level']]},")
            f.write(f"{label['name']}\n")