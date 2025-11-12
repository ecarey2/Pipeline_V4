import os
import glob
import pandas as pd

print('script is live')

def update_wide_region_file(region_df, curve_df):
    try:
        index_row = region_df[region_df.iloc[:, 0] == "Index"].index[0]
        starting_frame_row = region_df[region_df.iloc[:, 0] == "Starting Frame"].index[0]
    except:
        print("  ⚠ Could not locate 'Index' or 'Starting Frame' rows.")
        return region_df, False

    updated = False
    for col in range(1, region_df.shape[1]):
        try:
            event_id = int(region_df.iat[index_row, col])
            if event_id in curve_df['Event Index'].values:
                rise_time = curve_df[curve_df['Event Index'] == event_id]['10% Rise time'].values[0]
                region_df.iat[starting_frame_row, col] = rise_time
                updated = True
                print(f"  ✓ Updated Event ID {event_id} → col {col}")
        except Exception as e:
            print(f"  ⚠ Skipped column {col}: {e}")
            continue

    return region_df, updated

def update_region_files_by_event_id(region_dir, curve_dir, output_dir=None):
    print('function running')
    region_files = sorted(glob.glob(os.path.join(region_dir, "**/*.xlsx"), recursive=True))
    curve_files = sorted(glob.glob(os.path.join(curve_dir, "**/*.xlsx"), recursive=True))

    print(f"Found {len(curve_files)} curve files.")
    print(f"Found {len(region_files)} region files.")

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    for curve_path in curve_files:
        curve_name = os.path.splitext(os.path.basename(curve_path))[0].replace('_curves', '')
        curve_df = pd.read_excel(curve_path)
        curve_df['Event Index'] = curve_df['Event ID'].str.extract(r'(\d+)').astype(int)

        matching_region_files = [f for f in region_files if curve_name in os.path.basename(f)]

        print(f"\nProcessing curve file: {os.path.basename(curve_path)}")
        print(f"Matching region files: {[os.path.basename(f) for f in matching_region_files]}")

        for region_path in matching_region_files:
            region_df = pd.read_excel(region_path, header=None)
            updated_df, updated = update_wide_region_file(region_df, curve_df)

            if updated:
                output_path = (
                    os.path.join(output_dir, os.path.basename(region_path)) if output_dir
                    else region_path
                )
                updated_df.to_excel(output_path, index=False, header=False)
                print(f"  → Updated file saved to: {output_path}")
            else:
                print(f"  ⚠ No updates made to: {os.path.basename(region_path)}")

if __name__ == "__main__":
    region_dir = input("Enter path to the Region folder: ").strip().strip("'").strip('"')
    curve_dir = input("Enter path to the Curves folder: ").strip().strip("'").strip('"')
    output_dir = input("Enter path to the Output folder (leave blank to overwrite original files): ").strip().strip("'").strip('"')
    print(f"Region folder entered: '{region_dir}'")
    print(f"Curve folder entered: '{curve_dir}'")
    print(f"Output folder entered: '{output_dir}'")
    output_dir = output_dir if output_dir else None

    update_region_files_by_event_id(region_dir, curve_dir, output_dir)
