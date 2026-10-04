from key_expansion import key_expansion, sbox , gf_multiply , inv_s_box


def bytes_to_state(data):
    state = []

    for i in range(4):
        row = []

        for j in range(4):
            row.append(data[j * 4 + i])

        state.append(row)

    return state

def state_to_bytes(state):
    data = []

    for col in range(4):
        for row in range(4):
            data.append(state[row][col])

    return data



def sub_bytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = sbox(state[i][j])

    return state

def shift_rows(state):
    for i in range(4):
        state[i] = state[i][i:] + state[i][:i]

    return state

def mix_columns(state):

    for col in range(4):

        a = state[0][col]
        b = state[1][col]
        c = state[2][col]
        d = state[3][col]

        r0 = (gf_multiply(a, 0x02) ^ gf_multiply(b, 0x03) ^ c ^ d)

        r1 = (a ^ gf_multiply(b, 0x02) ^ gf_multiply(c, 0x03) ^ d)

        r2 = (a ^b ^ gf_multiply(c, 0x02) ^ gf_multiply(d, 0x03))

        r3 = (gf_multiply(a, 0x03) ^ b ^ c ^ gf_multiply(d, 0x02))

        state[0][col] = r0
        state[1][col] = r1
        state[2][col] = r2
        state[3][col] = r3

    return state

def add_round_key(state, round_key):
    for i in range(4):
        for j in range(4):
            state[i][j] ^= round_key[i][j]

    return state



def inv_sub_bytes(state):
    for row in range(4):
        for col in range(4):
            state[row][col] = inv_s_box[state[row][col]]

    return state

def inv_shift_rows(state):
    state[1] = state[1][-1:] + state[1][:-1]
    state[2] = state[2][-2:] + state[2][:-2]
    state[3] = state[3][-3:] + state[3][:-3]

    return state

def inv_mix_columns(state):

    for col in range(4):

        a0 = state[0][col]
        a1 = state[1][col]
        a2 = state[2][col]
        a3 = state[3][col]

        state[0][col] = (gf_multiply(a0, 0x0E) ^ gf_multiply(a1, 0x0B) ^ gf_multiply(a2, 0x0D) ^ gf_multiply(a3, 0x09))

        state[1][col] = (gf_multiply(a0, 0x09) ^ gf_multiply(a1, 0x0E) ^ gf_multiply(a2, 0x0B) ^ gf_multiply(a3, 0x0D))

        state[2][col] = (gf_multiply(a0, 0x0D) ^ gf_multiply(a1, 0x09) ^ gf_multiply(a2, 0x0E) ^ gf_multiply(a3, 0x0B))

        state[3][col] = (gf_multiply(a0, 0x0B) ^ gf_multiply(a1, 0x0D) ^ gf_multiply(a2, 0x09) ^ gf_multiply(a3, 0x0E))

    return state



def aes_round(state, round_key):
    state = sub_bytes(state)
    state = shift_rows(state)
    state = mix_columns(state)
    state = add_round_key(state, round_key)

    return state

def final_round(state, round_key):
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_key)

    return state

def make_round_keys(words):
    round_keys = []

    for i in range(0, 44, 4):

        words_for_round = words[i:i+4]

        round_key = []

        for row in range(4):

            current_row = []

            for word in words_for_round:
                current_row.append(word[row])

            round_key.append(current_row)

        round_keys.append(round_key)

    return round_keys



def aes_encrypt_block(block, key):

    state = bytes_to_state(block)

    words = key_expansion(key)
    round_keys = make_round_keys(words)

    # Initial AddRoundKey
    state = add_round_key(state, round_keys[0])

    # Rounds 1-9
    for round_number in range(1, 10):
        state = aes_round(state, round_keys[round_number])

    # Final round
    state = final_round(state, round_keys[10])

    return state_to_bytes(state)

def aes_decrypt_block(block, key):

    state = bytes_to_state(block)

    words = key_expansion(key)
    round_keys = make_round_keys(words)

    # Initial AddRoundKey with Round 10 key
    state = add_round_key(state, round_keys[10])

    # Rounds 9 → 1
    for round_number in range(9, 0, -1):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, round_keys[round_number])
        state = inv_mix_columns(state)

    # Final round
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    state = add_round_key(state, round_keys[0])

    return state_to_bytes(state)



