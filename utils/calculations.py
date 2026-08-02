import pandas as pd


EIHWAM_WEIGHTS = {
    "Level 1": 0,
    "Level 2": 2,
    "Level 3": 3,
    "Level 4": 4,
    "Level 5": 4,
    "Thesis": 8
}


def calculate_wam(df):

    completed = df[
        df["Status"] == "Completed"
    ]

    if completed.empty:
        return 0

    return (
        (completed["Mark"] * completed["CP"]).sum()
        /
        completed["CP"].sum()
    )


def calculate_eihwam(df):

    completed = df[
        df["Status"] == "Completed"
    ].copy()

    if completed.empty:
        return 0

    completed["Weight"] = (
        completed["Level"]
        .map(EIHWAM_WEIGHTS)
        .fillna(0)
    )

    numerator = (
        completed["Mark"]
        *
        completed["CP"]
        *
        completed["Weight"]
    ).sum()

    denominator = (
        completed["CP"]
        *
        completed["Weight"]
    ).sum()

    if denominator == 0:
        return 0

    return numerator / denominator


def calculate_projection(
    df,
    include_eihwam=True
):

    included = df[
        df["Status"].isin(
            ["Completed", "Remaining"]
        )
    ].copy()


    # WAM projection

    wam = (
        (included["Mark"] * included["CP"]).sum()
        /
        included["CP"].sum()
    )


    # EIHWAM projection

    included["Weight"] = (
        included["Level"]
        .map(EIHWAM_WEIGHTS)
        .fillna(0)
    )


    numerator = (
        included["Mark"]
        *
        included["CP"]
        *
        included["Weight"]
    ).sum()


    denominator = (
        included["CP"]
        *
        included["Weight"]
    ).sum()


    eihwam = (
        numerator / denominator
        if denominator != 0
        else 0
    )


    result = {
        "WAM": wam
    }


    if include_eihwam:
        result["EIHWAM"] = eihwam


    return result
def required_overall_average(df, target, metric="EIHWAM"):
    """
    Calculates the average needed across remaining units
    to hit a target.

    metric:
    - WAM
    - EIHWAM
    """

    completed = df[
        df["Status"] == "Completed"
    ].copy()

    remaining = df[
        df["Status"] == "Remaining"
    ].copy()


    if remaining.empty:
        return None


    if metric == "WAM":

        current_points = (
            completed["Mark"]
            *
            completed["CP"]
        ).sum()

        current_weight = (
            completed["CP"]
        ).sum()


        future_weight = (
            remaining["CP"]
        ).sum()


        required = (
            target * (current_weight + future_weight)
            - current_points
        ) / future_weight


    elif metric == "EIHWAM":

        completed["Weight"] = (
            completed["Level"]
            .map(EIHWAM_WEIGHTS)
            .fillna(0)
        )

        remaining["Weight"] = (
            remaining["Level"]
            .map(EIHWAM_WEIGHTS)
            .fillna(0)
        )


        current_points = (
            completed["Mark"]
            *
            completed["CP"]
            *
            completed["Weight"]
        ).sum()


        current_weight = (
            completed["CP"]
            *
            completed["Weight"]
        ).sum()


        future_weight = (
            remaining["CP"]
            *
            remaining["Weight"]
        ).sum()


        required = (
            target * (current_weight + future_weight)
            - current_points
        ) / future_weight


    else:
        return None


    return required

def required_group_averages(df, target_eihwam):

    completed = df[
        df["Status"] == "Completed"
    ].copy()

    remaining = df[
        df["Status"] == "Remaining"
    ].copy()


    if remaining.empty:
        return {}


    completed["Weight"] = (
        completed["Level"]
        .map(EIHWAM_WEIGHTS)
        .fillna(0)
    )

    remaining["Weight"] = (
        remaining["Level"]
        .map(EIHWAM_WEIGHTS)
        .fillna(0)
    )


    current_points = (
        completed["Mark"]
        *
        completed["CP"]
        *
        completed["Weight"]
    ).sum()


    current_weight = (
        completed["CP"]
        *
        completed["Weight"]
    ).sum()


    future_weight = (
        remaining["CP"]
        *
        remaining["Weight"]
    ).sum()


    results = {}


    for weight, group in remaining.groupby("Weight"):

        group_weight = (
            group["CP"]
            *
            weight
        ).sum()


        other_future_weight = (
            future_weight
            -
            group_weight
        )


        required = (
            target_eihwam
            *
            (
                current_weight
                +
                future_weight
            )
            -
            current_points
            -
            target_eihwam
            *
            other_future_weight
        ) / group_weight


        results[weight] = {
            "units": len(group),
            "cp": group["CP"].sum(),
            "required_average": required
        }


    return results