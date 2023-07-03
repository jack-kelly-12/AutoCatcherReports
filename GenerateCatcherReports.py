import pandas as pd
import matplotlib.pyplot as plt
import datetime

full_data = pd.read_csv('master.csv')
calls = ['StrikeCalled', 'BallCalled']
full_data = full_data[full_data['PitchCall'].isin(calls)]

strike_zone = {
    'x': [-1, 1, 1, -1, -1],
    'y': [1.5, 1.5, 3.5, 3.5, 1.5]
}

big_zone = {
    'x': [-1.15, 1.15, 1.15, -1.15, -1.15],
    'y': [1.35, 1.35, 3.65, 3.65, 1.35]
}

small_zone = {
    'x': [-.85, .85, .85, -.85, -.85],
    'y': [1.65, 1.65, 3.35, 3.35, 1.65]
}


def full_season_reports(catcher):
    catcher_data = full_data[full_data['Catcher'] == catcher]
    if len(catcher_data) == 0:
        print("No catcher data found. Try different name?")
        print("All catchers: ")
        print(full_data.Catcher.unique())
        return

    pitches_in_left = catcher_data[
        (catcher_data['PlateLocSide'] > big_zone['x'][0]) &
        (catcher_data['PlateLocSide'] <= small_zone['x'][0]) &
        (catcher_data['PlateLocHeight'] <= strike_zone['y'][2]) &
        (catcher_data['PlateLocHeight'] >= strike_zone['y'][0])
        ]

    pitches_in_right = catcher_data[
        (catcher_data['PlateLocSide'] < big_zone['x'][1]) &
        (catcher_data['PlateLocSide'] >= small_zone['x'][1]) &
        (catcher_data['PlateLocHeight'] <= strike_zone['y'][2]) &
        (catcher_data['PlateLocHeight'] >= strike_zone['y'][0])
        ]

    strikes_in_left = pitches_in_left[pitches_in_left['PitchCall'] == 'StrikeCalled']
    strikes_in_right = pitches_in_right[pitches_in_right['PitchCall'] == 'StrikeCalled']

    strike_count_left = len(strikes_in_left)
    strike_count_right = len(strikes_in_right)

    total_count_left = len(pitches_in_left)
    total_count_right = len(pitches_in_right)

    strike_total = pitches_in_left[pitches_in_left['PitchCall'] == 'StrikeCalled'].append(
        pitches_in_right[pitches_in_right['PitchCall'] == 'StrikeCalled'])

    ball_total = pitches_in_left[pitches_in_left['PitchCall'] == 'BallCalled'].append(
        pitches_in_right[pitches_in_right['PitchCall'] == 'BallCalled'])

    if total_count_left == 0 or total_count_right == 0:
        print("Not enough data")
        return

    percentage_left = (strike_count_left / total_count_left) * 100
    percentage_right = (strike_count_right / total_count_right) * 100

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.plot(strike_zone['x'], strike_zone['y'], color='black', linewidth=2)
    ax.plot(big_zone['x'], big_zone['y'], color='gray', linestyle='dashed', linewidth=1)
    ax.plot(small_zone['x'], small_zone['y'], color='gray', linestyle='dashed', linewidth=1)

    ax.scatter(
        strike_total['PlateLocSide'], strike_total['PlateLocHeight'],
        color='red', label='Strikes'
    )

    ax.scatter(
        ball_total['PlateLocSide'], ball_total['PlateLocHeight'],
        color='blue', label='Balls'
    )

    ax.set_title(f'{catcher}', fontsize=16)
    ax.set_xlabel('Horizontal Location', fontsize=12)
    ax.set_ylabel('Vertical Location', fontsize=12)

    ax.set_aspect('equal')
    ax.set_xlim([-2, 2])
    ax.set_ylim([1, 4])

    framing_runs = (len(ball_total) * -.125) + (len(strike_total) * .125)

    ax.text(
        0.20, 0.96, f'Left side K%: {percentage_left:.2f}%',
        transform=ax.transAxes, fontsize=12, color='black'
    )
    ax.text(
        0.20, 0.91, f'Right side K%: {percentage_right:.2f}%',
        transform=ax.transAxes, fontsize=12, color='black'
    )
    ax.text(
        .55, 0.91, f'Framing Runs: {framing_runs:.2f}',
        transform=ax.transAxes, fontsize=12, color='black'
    )

    ax.legend(loc='upper left')
    ax.grid(False)  # Turn off grid lines
    plt.show()


def single_game_report(catcher, game_date):
    catcher_data = full_data[full_data['Catcher'] == catcher]
    catcher_data = catcher_data[catcher_data['Date'] == str(datetime.datetime.strptime(game_date, "%Y%m%d").date())]
    if len(catcher_data) == 0:
        print("No catcher data found. Try different name or date?")
        return

    pitches_in_left = catcher_data[
        (catcher_data['PlateLocSide'] > big_zone['x'][0]) &
        (catcher_data['PlateLocSide'] <= small_zone['x'][0]) &
        (catcher_data['PlateLocHeight'] <= strike_zone['y'][2]) &
        (catcher_data['PlateLocHeight'] >= strike_zone['y'][0])
        ]

    pitches_in_right = catcher_data[
        (catcher_data['PlateLocSide'] < big_zone['x'][1]) &
        (catcher_data['PlateLocSide'] >= small_zone['x'][1]) &
        (catcher_data['PlateLocHeight'] <= strike_zone['y'][2]) &
        (catcher_data['PlateLocHeight'] >= strike_zone['y'][0])
        ]

    strikes_in_left = pitches_in_left[pitches_in_left['PitchCall'] == 'StrikeCalled']
    strikes_in_right = pitches_in_right[pitches_in_right['PitchCall'] == 'StrikeCalled']

    strike_count_left = len(strikes_in_left)
    strike_count_right = len(strikes_in_right)

    total_count_left = len(pitches_in_left)
    total_count_right = len(pitches_in_right)

    strike_total = pitches_in_left[pitches_in_left['PitchCall'] == 'StrikeCalled'].append(
        pitches_in_right[pitches_in_right['PitchCall'] == 'StrikeCalled'])

    ball_total = pitches_in_left[pitches_in_left['PitchCall'] == 'BallCalled'].append(
        pitches_in_right[pitches_in_right['PitchCall'] == 'BallCalled'])

    if total_count_left == 0 or total_count_right == 0:
        print("Not enough data")
        return

    percentage_left = (strike_count_left / total_count_left) * 100
    percentage_right = (strike_count_right / total_count_right) * 100

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.plot(strike_zone['x'], strike_zone['y'], color='black', linewidth=2)
    ax.plot(big_zone['x'], big_zone['y'], color='gray', linestyle='dashed', linewidth=1)
    ax.plot(small_zone['x'], small_zone['y'], color='gray', linestyle='dashed', linewidth=1)

    ax.scatter(
        catcher_data["PlateLocSide"], catcher_data["PlateLocHeight"],
        c=catcher_data["PitchCall"].map({'StrikeCalled': 'red', 'BallCalled': 'blue'}),
        label="Pitches"
    )

    ax.set_title(f'{catcher}', fontsize=16)
    ax.set_xlabel('Horizontal Location', fontsize=12)
    ax.set_ylabel('Vertical Location', fontsize=12)

    ax.set_aspect('equal')
    ax.set_xlim([-2, 2])
    ax.set_ylim([1, 4])

    ax.text(
        0.20, 0.96, f'Left side K%: {percentage_left:.2f}%',
        transform=ax.transAxes, fontsize=12, color='black'
    )
    ax.text(
        0.20, 0.91, f'Right side K%: {percentage_right:.2f}%',
        transform=ax.transAxes, fontsize=12, color='black'
    )

    ax.grid(False)  # Turn off grid lines
    plt.show()


def ask_for_input():
    catcher = input('Enter the name of the catcher you want a report for: ')
    type_letter = input('Enter (f) for full season catcher reports or (g) for one game catcher reports: ')
    if type_letter == 'f':
        full_season_reports(catcher)
    elif type_letter == 'g':
        game_date = input('Enter game date in (yyyymmdd) form: ')
        single_game_report(catcher, game_date)
    else:
        print("Invalid input")


def main():
    ask_for_input()


if __name__ == '__main__':
    main()
