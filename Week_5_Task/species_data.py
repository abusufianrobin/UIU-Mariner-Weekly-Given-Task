"""
eDNA Species Frequency Calculator
Holyrood Subsea Observatory - Frequency Analysis
"""

# Species data: name -> number seen
species_data = {
    "Snow crab (Chionecetes opilio)":                            19,
    "Acadian hermit crab (Pagurus acadianus)":                    3,
    "Western Atlantic Hairy Hermit Crab (Pagurus arcuatus)":      1,
    "European Green Crab (Carcinus maenas)":                      9,
    "Rock Crab (Cancer pagurus)":                                10,
    "Jonah Crab (Cancer borealis)":                               5,
    "Spiny Sunstar (Crossaster papposus)":                        8,
    "Sea Urchin (Strongylocentrotus droebachiensis)":            10,
    "Boreal Sea Star (Boreal asterias)":                         12,
    "Daisy brittle star (Ophiopholis aculeata)":                  7,
}

def calculate_percentage_frequency(data: dict) -> list[dict]:
    """
    Calculate percentage frequency for each species.

    Formula: % Frequency = (Number Seen / Total Seen) x 100
    """
    total = sum(data.values())
    results = []
    for species, count in data.items():
        pct = (count / total) * 100
        results.append({
            "species":       species,
            "number_seen":   count,
            "pct_frequency": pct,
        })
    return results, total


def print_table(results: list[dict], total: int) -> None:
    """Print results in a formatted table."""

    # Column widths
    col1 = 55   # Species
    col2 = 14   # Number Seen
    col3 = 16   # % Frequency

    border = "+" + "-" * col1 + "+" + "-" * col2 + "+" + "-" * col3 + "+"
    header = (
        f"| {'Species':<{col1-2}} | {'Number Seen':^{col2-2}} | {'% Frequency':^{col3-2}} |"
    )

    print("\n" + "=" * len(border))
    print("   Holyrood Subsea Observatory — Species Percentage Frequency")
    print("=" * len(border))
    print(border)
    print(header)
    print(border.replace("-", "="))

    for row in results:
        species_str = row["species"]
        # Wrap long species names across two lines
        if len(species_str) > col1 - 2:
            line1 = species_str[: col1 - 2]
            line2 = species_str[col1 - 2:]
            print(f"| {line1:<{col1-2}} | {row['number_seen']:^{col2-2}} | {row['pct_frequency']:^{col2}.8f} |")
            print(f"| {'  ' + line2:<{col1-2}} | {'':<{col2-2}} | {'':<{col2-2}} |")
        else:
            print(
                f"| {species_str:<{col1-2}} "
                f"| {row['number_seen']:^{col2-2}} "
                f"| {row['pct_frequency']:{col3-2}.8f} |"
            )
        print(border)

    # Totals row
    total_row = (
        f"| {'TOTAL':<{col1-2}} "
        f"| {total:^{col2-2}} "
        f"| {'100.00000000':^{col2-2}} |"
    )
    print(total_row)
    print(border)
    print(f"\n  Total species observed: {total}")
    print(f"  Number of species:      {len(results)}\n")


def main():
    results, total = calculate_percentage_frequency(species_data)
    print_table(results, total)

    # Verification output
    print("  Verification (sample):")
    first = results[0]
    print(
        f"  {first['species']}: "
        f"{first['number_seen']} / {total} × 100 = "
        f"{first['pct_frequency']:.8f}%\n"
    )


if __name__ == "__main__":
    main()