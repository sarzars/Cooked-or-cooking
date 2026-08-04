EIHWAM_WEIGHTS = {
    "Level 1": 0,
    "Level 2": 2,
    "Level 3": 3,
    "Level 4": 4,
    "Level 5": 4,
    "Thesis": 8,
}

EIHWAM_LABELS = {
    0: "Level 1 units",
    2: "Level 2 units",
    3: "Level 3 units",
    4: "Level 4/5 units",
    8: "Thesis units",
}


def _weighted_average(data, mark_column, weight_column="CP"):
    denominator = data[weight_column].sum()
    if denominator == 0:
        return 0
    return (data[mark_column] * data[weight_column]).sum() / denominator


def _completed_units(df):
    return df.loc[df["Status"] == "Completed"].copy()


def _projected_units(df):
    units = df.loc[df["Status"].isin(["Completed", "Remaining"])].copy()
    units["Effective Mark"] = units["Mark"].where(
        units["Status"] == "Completed",
        units["Projected Mark"],
    )
    return units


def _add_eihwam_weight(df):
    weighted = df.copy()
    weighted["Weight"] = (
        weighted["Level"].map(EIHWAM_WEIGHTS).fillna(0).astype(float)
    )
    weighted["EIHWAM CP"] = weighted["CP"] * weighted["Weight"]
    return weighted


def calculate_wam(df):
    """Current WAM: completed units only, using their actual Mark."""
    return _weighted_average(_completed_units(df), "Mark")


def calculate_eihwam(df):
    """Current EIHWAM: completed units only, using their actual Mark."""
    return _weighted_average(
        _add_eihwam_weight(_completed_units(df)), "Mark", "EIHWAM CP"
    )


def calculate_projection(df, include_eihwam=True):
    """Projected results use Mark for completed and Projected Mark for remaining."""
    projected = _projected_units(df)
    result = {"WAM": _weighted_average(projected, "Effective Mark")}

    if include_eihwam:
        weighted = _add_eihwam_weight(projected)
        result["EIHWAM"] = _weighted_average(
            weighted, "Effective Mark", "EIHWAM CP"
        )

    return result


def required_overall_average(df, target, metric="EIHWAM"):
    completed = _completed_units(df)
    remaining = df.loc[df["Status"] == "Remaining"].copy()

    if remaining.empty:
        return None

    if metric == "WAM":
        current_weight = completed["CP"].sum()
        future_weight = remaining["CP"].sum()
        current_points = (completed["Mark"] * completed["CP"]).sum()
    elif metric == "EIHWAM":
        completed = _add_eihwam_weight(completed)
        remaining = _add_eihwam_weight(remaining)
        current_weight = completed["EIHWAM CP"].sum()
        future_weight = remaining["EIHWAM CP"].sum()
        current_points = (completed["Mark"] * completed["EIHWAM CP"]).sum()
    else:
        raise ValueError("metric must be WAM or EIHWAM")

    if future_weight == 0:
        return None

    return (
        target * (current_weight + future_weight) - current_points
    ) / future_weight


def required_group_averages(df, target_eihwam):
    completed = _add_eihwam_weight(_completed_units(df))
    remaining = _add_eihwam_weight(
        df.loc[df["Status"] == "Remaining"].copy()
    )

    if remaining.empty:
        return {}

    current_points = (completed["Mark"] * completed["EIHWAM CP"]).sum()
    current_weight = completed["EIHWAM CP"].sum()
    future_weight = remaining["EIHWAM CP"].sum()
    results = {}

    for weight, group in remaining.groupby("Weight"):
        group_weight = group["EIHWAM CP"].sum()
        if group_weight == 0:
            continue

        other_future_weight = future_weight - group_weight
        required = (
            target_eihwam * (current_weight + future_weight)
            - current_points
            - target_eihwam * other_future_weight
        ) / group_weight

        results[weight] = {
            "units": len(group),
            "cp": group["CP"].sum(),
            "required_average": required,
        }

    return results


def eihwam_target_scenarios(df, target):
    """Create distinct unit-level mark plans that exactly meet an EIHWAM target."""
    completed = _add_eihwam_weight(_completed_units(df))
    remaining = _add_eihwam_weight(
        df.loc[df["Status"] == "Remaining"].copy()
    )

    future_weight = remaining["EIHWAM CP"].sum()
    if remaining.empty or future_weight == 0:
        return {}

    total_weight = completed["EIHWAM CP"].sum() + future_weight
    completed_points = (completed["Mark"] * completed["EIHWAM CP"]).sum()
    required_average = (target * total_weight - completed_points) / future_weight

    if not 0 <= required_average <= 100:
        return {}

    balanced = df.copy()
    balanced.loc[balanced["Status"] == "Remaining", "Projected Mark"] = (
        required_average
    )

    higher_level_focus = balanced.copy()
    impactful = remaining.loc[remaining["EIHWAM CP"] > 0].copy()
    weighted_mean_level = (
        (impactful["Weight"] * impactful["EIHWAM CP"]).sum()
        / impactful["EIHWAM CP"].sum()
    )
    pattern = impactful["Weight"] - weighted_mean_level

    positive_limits = [
        (100 - required_average) / value for value in pattern if value > 0
    ]
    negative_limits = [
        required_average / -value for value in pattern if value < 0
    ]
    maximum_scale = min([3, *positive_limits, *negative_limits])
    higher_level_focus.loc[impactful.index, "Projected Mark"] = (
        required_average + maximum_scale * pattern
    )

    return {
        "Balanced target plan": balanced,
        "Higher-level-unit focus": higher_level_focus,
    }


def eihwam_unit_impact(df):
    """Show each remaining unit's EIHWAM leverage for a one-mark increase."""
    weighted = _add_eihwam_weight(_projected_units(df))
    total_weight = weighted["EIHWAM CP"].sum()
    remaining = weighted.loc[weighted["Status"] == "Remaining"].copy()

    if total_weight == 0:
        return remaining.iloc[0:0]

    impact = remaining[
        ["Unit", "Semester", "Level", "CP", "Weight", "EIHWAM CP"]
    ].copy()
    impact["EIHWAM gain per +1 projected mark"] = (
        impact["EIHWAM CP"] / total_weight
    )
    return impact.sort_values(
        "EIHWAM gain per +1 projected mark", ascending=False
    )
