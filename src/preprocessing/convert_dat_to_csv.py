import os
import subprocess


# =========================================================
# CONVERT DAT TO CSV
# =========================================================

def convert_dat_to_csv(
    dat2csv_path,
    dat_path,
    output_csv_dir,
):

    os.makedirs(
        output_csv_dir,
        exist_ok=True,
    )

    scenario_name = os.path.splitext(
        os.path.basename(dat_path)
    )[0]

    csv_output_path = os.path.join(
        output_csv_dir,
        f"{scenario_name}.csv",
    )

    # -----------------------------------------------------
    # DAT2CSV COMMAND
    # -----------------------------------------------------

    cmd = [

        dat2csv_path,

        "--file",
        dat_path,

        "--csv",
        csv_output_path,

        "--extended",
    ]

    print(
        "\n================================================="
    )

    print(
        f"Converting DAT to CSV:\n"
    )

    print(
        " ".join(cmd)
    )

    print(
        "\n=================================================\n"
    )

    # -----------------------------------------------------
    # EXECUTE
    # -----------------------------------------------------

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    # -----------------------------------------------------
    # STDOUT
    # -----------------------------------------------------

    if result.stdout:

        print(result.stdout)

    # -----------------------------------------------------
    # STDERR
    # -----------------------------------------------------

    if result.stderr:

        print(result.stderr)

    # -----------------------------------------------------
    # SUCCESS CHECK
    # -----------------------------------------------------

    if result.returncode != 0:

        raise RuntimeError(
            f"\nDAT to CSV conversion failed "
            f"for:\n{dat_path}\n"
        )

    # -----------------------------------------------------
    # VERIFY CSV EXISTS
    # -----------------------------------------------------

    if not os.path.exists(
        csv_output_path
    ):

        raise FileNotFoundError(
            f"\nExpected CSV output not found:\n"
            f"{csv_output_path}\n"
        )

    print(
        f"\nGenerated CSV:\n"
        f"{csv_output_path}\n"
    )

    return csv_output_path