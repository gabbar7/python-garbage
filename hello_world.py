#!/usr/bin/env python3
from copy import deepcopy
from collections import Counter
from random import randint

RESET_AT_ROUND = 15
RESET_AT_RECOMMENDATION = 15
RESET_IF_EMPTY = 9
RESET_TOO_LONG = 9


# CONSTANTS
MINIMUM_ROI = 1
WIN_MULTIPLIER = 29
# WIN_MULTIPLIER = 35

RACETRACK = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

TABLES = [
     [17,  1, 35, 34,  3, 32], [ 6, 30,  8, 28, 27, 11], [ 7, 24, 23, 15, 16, 14], [19, 13,  2, 21, 10, 20], [18, 12, 26,  9, 22, 29], [25, 31, 36,  4, 33,  5], [17,  6,  7, 19, 18, 25], [ 1, 30, 24, 13, 12, 31], [35,  8, 23,  2, 26, 36], [34, 28, 15, 21,  9,  4], [ 3, 27, 16, 10, 22, 33], [32, 11, 14, 20 ,29,  5], [17, 30, 23, 21, 22,  5], [32, 27, 15,  2, 12, 25] # cartella 1
    ,[36, 14,  4, 13, 22, 31], [23, 34, 29, 32,  9,  3], [ 8, 25, 28,  1, 10, 12], [17, 16, 11, 19, 20, 21], [26,  7,  2, 27, 18, 30], [35,  5, 33, 24, 15,  6], [36, 23,  8, 17, 26, 35], [14, 34, 25, 16,  7,  5], [ 4, 29, 28, 11,  2, 33], [13, 32,  1, 19, 27, 24], [22,  9, 10, 20, 18, 15], [31,  3, 12, 21, 30,  6], [36, 34, 28, 19, 18,  6], [31,  9,  1, 11,  7, 35] # cartella 2
    ,[ 2, 34, 10, 21, 13, 28], [ 6,  9, 19,  5, 36, 32], [27, 35, 23, 26, 14, 11], [20, 31, 25, 16,  7,  3], [12,  4, 17,  1, 15, 24], [22, 33,  8, 30, 18, 29], [ 2,  6, 27, 20, 12, 22], [34,  9, 35, 31,  4, 33], [10, 19, 23, 25, 17,  8], [21,  5, 26, 16,  1, 30], [13, 36, 14,  7, 15, 18], [28, 32, 11,  3, 24, 29], [ 2,  9, 23, 16, 15, 29], [22,  4, 25, 26, 36, 28] # cartella 3
    ,[ 2,  1, 35, 16, 21, 34], [ 4, 32,  6, 20, 17,  7], [29, 25, 26,  9, 10, 23], [18, 12, 11, 27, 28, 14], [19,  8, 30, 24, 13, 31], [ 5, 33,  3, 15, 22, 36], [ 2,  4, 29, 18, 19,  5], [ 1, 32, 25, 12,  8, 33], [35,  6, 26, 11, 30,  3], [16, 20,  9, 27, 24, 15], [21, 17, 10, 28, 13, 22], [34,  7, 23, 14, 31, 36], [ 2, 32, 26, 27, 13, 36], [ 5,  8, 11,  9, 17, 34] # cartella 4
    ,[26, 14, 22,  6, 25,  2], [34, 30,  3, 17, 23,  5], [11, 29, 35, 21,  9, 13], [33, 15, 18, 20, 28, 31], [27,  7, 24,  4,  1, 16], [10, 36, 12, 19, 32,  8], [26, 34, 11, 33, 27, 10], [14, 30, 29, 15,  7, 36], [22,  3, 35, 18, 24, 12], [ 6, 17, 21, 20,  4, 19], [25, 23,  9, 28,  1, 32], [ 2,  5, 13, 31, 16,  8], [26, 30, 35, 20,  1,  8], [10,  7, 18, 21, 23,  2] # cartella 5
    ,[31, 14, 36,  8, 22, 15], [ 9, 24, 30, 35, 28, 21], [12,  6, 33, 17, 27, 13], [10, 23,  2,  7, 20, 34], [11, 32,  5, 18,  4, 26], [19,  3, 16, 29,  1, 25], [31,  9, 12, 10, 11, 19], [14, 24,  6, 23, 32,  3], [36, 30, 33,  2,  5, 16], [ 8, 35, 17,  7, 18, 29], [22, 28, 27, 20,  4,  1], [15, 21, 13, 34, 26, 25], [31, 24, 33,  7,  4, 25], [19, 32,  2, 17, 28, 15] # cartella 6
    ,[ 1, 13, 30, 22, 24, 17], [12, 14,  5, 18, 15, 32], [26, 34, 10, 33,  3,  9], [20, 28,  8,  6, 29, 19], [23, 11,  4, 27, 31,  7], [16, 36, 35, 25,  2, 21], [ 1, 12, 26, 20, 23, 16], [13, 14, 34, 28, 11, 36], [30,  5, 10,  8,  4, 35], [22, 18, 33,  6, 27, 25], [24, 15,  3, 29, 31,  2], [17, 32,  9, 19,  7, 21], [ 1, 14, 10,  6, 31, 21], [16, 11,  8, 33, 15, 17] # cartella 7
    # ,[ 7, 32, 15, 19,  4, 21], [ 2, 13, 27,  6, 34, 17], [25, 36, 11, 30,  8, 23], [10, 20,  1, 33, 16, 24], [ 5, 14, 31,  9, 22, 18], [29, 26,  3, 35, 12, 28], [ 7,  2, 25, 10,  5, 29], [32, 13, 36, 20, 14, 26], [15, 27, 11,  1, 31,  3], [19,  6, 30, 33,  9, 35], [ 4, 34,  8, 16, 22, 12], [21, 17, 23, 24, 18, 28], [ 7, 13, 11, 33, 22, 28], [29, 14,  1, 30, 34, 21] # cartella 8
    # ,[14, 23, 10, 11,  1, 34], [ 5,  7, 24, 18, 16, 27], [12, 15, 19, 36,  9, 13], [21, 28, 33,  4, 26, 29], [17,  8, 20, 32, 25,  3], [35,  6,  2, 30, 22, 31], [14,  5, 12, 21, 17, 35], [23,  7, 15, 28,  8,  6], [10, 24, 19, 33, 20,  2], [11, 18, 36,  4, 32, 30], [ 1, 16,  9, 26, 25, 22], [34, 27, 13, 29,  3, 31], [14,  7, 19,  4, 25, 31], [35,  8, 33, 36, 16, 34] # cartella 9
    # ,[36, 35, 34, 33, 32, 31], [30, 29, 28, 27, 26, 25], [24, 23, 22, 21, 20, 19], [18, 17, 16, 15, 14, 13], [12, 11, 10,  9,  8,  7], [ 6,  5,  4,  3,  2,  1], [36, 30, 24, 18, 12,  6], [35, 29, 23, 17, 11,  5], [34, 28, 22, 16, 10,  4], [33, 27, 21, 15,  9,  3], [32, 26, 20, 14,  8,  2], [31, 25, 19, 13,  7,  1], [36, 29, 22, 15,  8,  1], [ 6, 11, 16, 21, 26, 31] # cartella 10
    # ,[19, 25,  7,  3, 26, 20], [24,  2, 32, 31,  8, 27], [12, 33, 13, 14, 30,  4], [ 1, 34, 16, 15, 29,  9], [23, 11, 35, 36,  5, 28], [18, 22,  6, 10, 21, 17], [19, 24, 12,  1, 23, 18], [25,  2, 33, 34, 11, 22], [ 7, 32, 13, 16, 35,  6], [ 3, 31, 14, 15, 36, 10], [26,  8, 30, 29,  5, 21], [20, 27,  4,  9, 28, 17], [19,  2, 13, 15,  5, 17], [18, 11, 16, 14,  8, 20] # cartella 11
    # ,[ 4, 30,  9, 19,  7, 33], [11, 24,  2, 35, 21, 25], [12, 27, 32,  5, 15, 17], [16, 14,  6, 31, 28, 13], [26, 22, 34,  3, 23, 20], [36,  8, 18, 10, 29,  1], [ 4, 11, 12, 16, 26, 36], [30, 24, 27, 14, 22,  8], [ 9,  2, 32,  6, 34, 18], [19, 35,  5, 31,  3, 10], [ 7, 21, 15, 28, 23, 29], [33, 25, 17, 13, 20,  1], [ 4, 24, 32, 31, 23,  1], [36, 22,  6,  5, 21, 33] # cartella 12
    # ,[18, 31, 17,  1,  4,  9], [ 3, 10, 20, 24, 15,  7], [36,  5, 23, 11, 33, 25], [14, 35,  8, 26, 22, 28], [19, 13,  6, 16, 32, 21], [30, 12, 34, 28, 27,  2], [18,  3, 36, 14, 19, 30], [31, 10,  5, 35, 13, 12], [17, 20, 23,  8,  6, 34], [ 1, 24, 11, 26, 16, 28], [ 4, 15, 33, 22, 32, 27], [ 9,  7, 25, 28, 21,  2], [18, 10, 23, 26, 32,  2], [30, 13,  8, 11, 15,  9] # cartella 13
    # ,[31, 28, 15, 24, 36, 18], [12, 10, 32,  6, 23,  4], [29, 33, 19, 11,  5, 27], [ 8,  9, 21,  1,  2, 22], [34, 17, 25,  7, 14, 30], [16, 13, 20, 26, 35,  3], [31, 12, 29,  8, 34, 16], [28, 10, 33,  9, 17, 13], [15, 32, 19, 21, 25, 20], [24,  6, 11,  1,  7, 26], [36, 23,  5,  2, 14, 35], [18,  4, 27, 22, 30,  3], [31, 10, 19,  1, 14,  3], [16, 17, 21, 11, 23, 18] # cartella 14
    # ,[25, 10, 19,  9,  4, 14], [36,  5, 15, 20, 18, 29], [ 8, 35, 27, 31, 21, 32], [22, 30, 17, 16, 26,  7], [33,  3, 12,  6,  2, 28], [23, 24, 34, 13, 11,  1], [25, 36,  8, 22, 33, 23], [10,  5, 35, 30,  3, 24], [19, 15, 27, 17, 12, 34], [ 9, 20, 31, 16,  6, 13], [ 4, 18, 21, 26,  2, 11], [14, 29, 32,  7, 28,  1], [25,  5, 27, 16,  2,  1], [23,  3, 17, 31, 18, 14] # cartella 15
]

def count_repetitions(cr_counter):
    cr_counter = Counter(cr_counter)
    cr_singles = []
    cr_doubles = []
    cr_triples = []
    for k, v in cr_counter.items():
        if v > 2:
            cr_triples.append(k)
        elif v > 1:
            cr_doubles.append(k)
        else:
            cr_singles.append(k)
    return cr_singles, cr_doubles, cr_triples

def get_unique_numbers(f_numbers):
    list_of_unique_numbers = []
    # unique_numbers = set(f_numbers)
    for number in f_numbers:
        if number not in list_of_unique_numbers:
            list_of_unique_numbers.append(number)
    list_of_unique_numbers.sort()
    return list_of_unique_numbers

def create_recommendations(f_session_results, f_tables):
    # remove from the matrix the recommendations stored in "session_results"
    f_recommendations = []
    for i in range(len(f_session_results)):
            for n in range(len(f_tables)):
                for l in range(len(f_tables[n])):
                    if f_session_results[i] in f_tables[n]:
                        spin_result_idx = f_tables[n].index(f_session_results[i])
                        if 'spin_result_idx' in locals():
                            f_tables[n].pop(spin_result_idx)
                            del(spin_result_idx)
                            f_recommendations = []

    for n in range(len(f_tables)):
        # if len(f_tables[n]) <= 2:
        if len(f_tables[n]) == 2:
            # min_len = len(f_tables[n])
            f_recommendations.append(f_tables[n][0])
            if len(f_tables[n]) == 2:
                f_recommendations.append(f_tables[n][1])
            f_recommendations = get_unique_numbers(f_recommendations)

    if len(f_recommendations) >= 1:
        singles, doubles, triples = count_repetitions(f_session_results)
        del singles
        if len(doubles) > 0 or len(triples) > 0 :
            for d in range(len(doubles)):
                f_recommendations.append(doubles[d])
            for t in range(len(triples)):
                f_recommendations.append(triples[t])

    return f_tables, f_recommendations

def evaluate_bet(f_len_recommendation, f_exposure):
    # Evaluates the bet based on:
    # - the exposure
    # - the amount of number to bet on
    # - the desired ROI
    # - the payout
    roi = f_chips = 0
    while roi < MINIMUM_ROI:
        f_chips += 1
        roi = WIN_MULTIPLIER * f_chips - (f_exposure + f_len_recommendation * f_chips)
    # if f_chips > 0:
    #     print('\tChips: {} | Expected ROI: {}'.format(f_chips, roi))

    f_exposure += f_chips * f_len_recommendation
    return f_chips, f_exposure

def is_neighbor(f_recommendations, f_spin_result):
    # Check if the result is neighbor of a recommendation
    f_neighbors = []
    for n in range(len(f_recommendations)):
        # print(f_unique_prediction[n])
        pos = RACETRACK.index(f_recommendations[n])
        n_1a = (pos - 1) % len(RACETRACK)
        n_1b = (pos + 1) % len(RACETRACK)
        f_neighbors.append(RACETRACK[n_1a])
        f_neighbors.append(RACETRACK[n_1b])

        # n_2a = (pos - 2) % len(RACETRACK)
        # n_2b = (pos + 2) % len(RACETRACK)
        # f_neighbors.append(RACETRACK[n_2a])
        # f_neighbors.append(RACETRACK[n_2b])

        # n_3a = (pos - 3) % len(RACETRACK)
        # n_3b = (pos + 3) % len(RACETRACK)
        # f_neighbors.append(RACETRACK[n_3a])
        # f_neighbors.append(RACETRACK[n_3b])
    f_neighbors_2 = []
    if len(f_neighbors) > 0:
        for n in range(len(f_neighbors)):
            if f_neighbors[n] not in f_recommendations:
                # f_neighbors.pop(n)
                f_neighbors_2.append(f_neighbors[n])

    if f_spin_result in f_neighbors_2:
        return True
    else:
        return False

    # return(f_neighbors)

def reset_at(f_session_results, f_full_session_lenght, f_recommendations, f_reset_to, f_reset_count, f_chips, f_exposure):
    # shorten the session to f_reset_to results
    while len(f_session_results) > f_reset_to :
        f_session_results.pop(0)
    # print('RESET')
    # f_singles, f_doubles, f_triples = count_repetitions(f_session_results)
    # f_repeated = len(f_doubles)+len(f_triples)

    # wrp_stats_CSV = open(OUTPUT_CSV, 'a', encoding="utf-8")
    # wrp_stats_line = '{},{},{},{},"{}","{}",{},{},"RESET"\n'\
    #     .format(len(f_full_session_lenght), f_repeated, len(f_recommendations), len(f_full_session_lenght)-f_repeated\
    #             , f_full_session_lenght, f_recommendations, f_chips, f_exposure)

    # wrp_stats_CSV.write(wrp_stats_line)
    # wrp_stats_CSV.close()
    f_reset_count += 1
    return f_session_results, f_reset_count


if __name__ == '__main__':
    historical_data = []
    for i in range(10000):
        historical_data.append(randint(0,36))

    # wrp_stats_CSV = open(OUTPUT_CSV, 'w', encoding="utf-8")
    # header = 'session_length,doubles,recommendations,unique_numbers,session_results,recommendations,chips,exposure,"gotcha/miss"\n'
    # wrp_stats_CSV.write(header)

    # wrp_stats_CSV.close()

    tables = deepcopy(TABLES)

    min_len = 99
    session_results = []
    max_num_to_bet_on = 0
    recommendations = []
    doubles = []
    triples = []
    rec_last_5 = []
    is_looping = True
    spin_result = 0
    max_exposure = current_exposure = 0

    reset_count = 0
    full_session_lenght = []
    
    for h in range(len(historical_data)-1):
        spin_result = historical_data[h]
        session_results.append(spin_result)
        full_session_lenght.append(spin_result)

        units_to_be_per_number, current_exposure = evaluate_bet(len(recommendations), current_exposure)

        if spin_result in recommendations or spin_result in triples:
            singles, doubles, triples = count_repetitions(session_results)
            repeated = len(doubles)+len(triples)

            singles, doubles, triples = count_repetitions(session_results)
            repeated = len(doubles)+len(triples)
            # BAZOOOKA # print("GOTCHA")

            wrp_stats_line = '{},{},{},{},"{}","{}", {}, {}, "GOTCHA"\n'\
                .format(len(session_results), repeated, max_num_to_bet_on, len(full_session_lenght)-repeated\
                        , session_results, recommendations, max_num_to_bet_on, current_exposure)

            max_exposure = max(max_exposure, current_exposure)
            max_num_to_bet_on = 0
            current_exposure = 0
            tables = deepcopy(TABLES)
            min_len = 99
            recommendations  = []
            session_results = []
            full_session_lenght = []
            singles, doubles, triples = [], [], []
            reset_count = 0

        else:
            # remove from the matrix the recommendations stored in "session_results"
            for n in range(len(tables)):
                for l in range(len(tables[n])):
                    if spin_result in tables[n]:
                        spin_result_idx = tables[n].index(spin_result)
                        if 'spin_result_idx' in locals():
                            tables[n].pop(spin_result_idx)
                            del(spin_result_idx)

            # RESET IF NEIGHBOR
            if is_neighbor(recommendations, spin_result) and reset_count > 0:
                # BAZOOOKA # print('RESET IF NEIGHBOR')
                session_results, reset_count = reset_at(session_results, full_session_lenght, recommendations\
                                                        , min_reset, reset_count, units_to_be_per_number, current_exposure)
                tables = deepcopy(TABLES)
                singles, doubles, triples = [], [], []
                recommendations = []
                max_num_to_bet_on = 0

            # RESET IF EMPTY
            elif len(recommendations) == 0 and len(session_results) >= 10:
                # BAZOOOKA # print('POPPING STALES')
                tables = deepcopy(TABLES)
                session_results, reset_count = reset_at(session_results, full_session_lenght, recommendations\
                                                        , RESET_IF_EMPTY, reset_count, units_to_be_per_number, current_exposure)
                singles, doubles, triples = [], [], []
                recommendations = []
                max_num_to_bet_on = 0

            # RESET IF TOO LONG
            elif len(session_results) >= RESET_AT_ROUND or max_num_to_bet_on >= RESET_AT_RECOMMENDATION:
                # BAZOOOKA # print('RESET IF TOO LONG')
                tables = deepcopy(TABLES)
                session_results, reset_count = reset_at(session_results, full_session_lenght, recommendations\
                                                        , RESET_TOO_LONG, reset_count, units_to_be_per_number, current_exposure)
                singles, doubles, triples = [], [], []
                recommendations = []
                max_num_to_bet_on = 0

            # populate the recommendations list
            tables, recommendations = create_recommendations(session_results, tables)

            if len(recommendations) > max_num_to_bet_on:
                max_num_to_bet_on = len(recommendations)

            if max_num_to_bet_on >= 2:
                repetitions = deepcopy(session_results)
                singles, doubles, triples = count_repetitions(repetitions)
                if len(doubles) > 0 or len(triples) > 0 :
                    for d in range(len(doubles)):
                        recommendations.append(doubles[d])
                    for t in range(len(triples)):
                        recommendations.append(triples[t])

            # Count the numbers
            recommendations = get_unique_numbers(recommendations)
            max_num_to_bet_on = len(recommendations)
            repeated = len(doubles)+len(triples)

            # nicer, but there's still an issue if I want to store this in the stats file ##
            min_reset = 99
            for last_n in range(5, len(session_results)+1):
                # if len(session_results) >= last_n:
                tables_last_n = deepcopy(TABLES)
                tables_last_n, rec_last_n = create_recommendations(session_results[-last_n:], tables_last_n)
                if len(rec_last_n) > 0: #and last_n < min_reset:
                    min_reset = min(min_reset, last_n-1)

            if 'tables_last_n' in locals():
                del tables_last_n

    print(max_exposure)
