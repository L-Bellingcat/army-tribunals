import pandas as pd
from ydata_profiling import ProfileReport


def make_report(region: str):
    # Load structured_judgements/Chandigarh.csv into DataFrame
    region_data = pd.read_csv(f'structured_judgements/{region}.csv')

    # Run PandasProfiling on the DataFrame
    profile = ProfileReport(region_data, title=f'{region} judgements')

    profile.to_file(f"{region}_report.html")

    # names = region_data['military_judge'].values

    # # Remove duplicates
    # names = list(set(names))
    #
    # # Save to txt file
    # with open('military_judges.txt', 'w') as f:
    #     for name in names:
    #         f.write(name + '\n')
    #
    # # Civilian judges
    # names = region_data['civilian_judge'].values
    #
    # # Remove duplicates
    # names = list(set(names))
    #
    # # Save to txt file
    # with open('civilian_judges.txt', 'w') as f:
    #     for name in names:
    #         f.write(name + '\n')


def main():
    make_report('chandigarh')
    make_report('lucknow')


if __name__ == '__main__':
    main()
