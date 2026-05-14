import os
import subprocess


# =========================================================
# RUN ESMINI HEADLESS
# =========================================================

def run_esmini_headless(
    esmini_path,
    xosc_path,
    output_log_dir,
):

    os.makedirs(
        output_log_dir,
        exist_ok=True,
    )

    scenario_name = os.path.splitext(
        os.path.basename(xosc_path)
    )[0]

    dat_output_path = os.path.join(
        output_log_dir,
        f"{scenario_name}.dat",
    )

    # -----------------------------------------------------
    # ESMINI COMMAND
    # -----------------------------------------------------

    cmd = [

        esmini_path,

        "--osc",
        xosc_path,

        "--headless",

        "--fixed_timestep",
        "0.05",

        "--record",
        dat_output_path,
    ]

    print(
        "\n================================================="
    )

    print(
        f"Running esmini headless:\n"
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
            f"\nesmini execution failed "
            f"for:\n{xosc_path}\n"
        )

    # -----------------------------------------------------
    # VERIFY DAT EXISTS
    # -----------------------------------------------------

    if not os.path.exists(
        dat_output_path
    ):

        raise FileNotFoundError(
            f"\nExpected DAT output not found:\n"
            f"{dat_output_path}\n"
        )

    print(
        f"\nGenerated DAT log:\n"
        f"{dat_output_path}\n"
    )

    return dat_output_path