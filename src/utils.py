def format_bytes(bytes_):
    tb = bytes_ // 1099511627776
    bytes_ %= 1099511627776

    gb = bytes_ // 1073741824
    bytes_ %= 1073741824

    mb = bytes_ // 1048576
    bytes_ %= 1048576

    kb = bytes_ // 1024
    bytes_ %= 1024

    if tb + gb + mb + kb + bytes_ == 0:
        return '0B'
    else:
        if tb > 0:
            tb = f'{tb}TB '
        else:
            tb = ''

        if gb > 0:
            gb = f'{gb}GB '
        else:
            gb = ''

        if mb > 0:
            mb = f'{mb}MB '
        else:
            mb = ''            

        if kb > 0:
            kb = f'{kb}KB '
        else:
            kb = ''            

        if bytes_ > 0:
            bytes_ = f'{bytes_}B'
        else:
            bytes_ = ''

        return f'{tb}{gb}{mb}{kb}{bytes_}'.strip()
