import customtkinter as ctk



def get_status(
        value,
        minimum,
        maximum,
        optimal,
        direction="range"
):

    optimal_low, optimal_high = optimal


    # -----------------------------------
    # Außerhalb gültiger Grenzen
    # -----------------------------------

    if value < minimum:

        return (
            "Too Low",
            "#D9534F"
        )


    if value > maximum:

        return (
            "Too High",
            "#D9534F"
        )



    # -----------------------------------
    # Optimalbereich
    # -----------------------------------

    if optimal_low <= value <= optimal_high:

        return (
            "Optimal",
            "#5CB85C"
        )



    # -----------------------------------
    # Toleranzbereich
    # -----------------------------------

    total_range = maximum - minimum

    tolerance = total_range * 0.15



    # Unterhalb optimal

    if value < optimal_low:

        difference = optimal_low - value


        if difference <= tolerance:

            return (
                "Slightly Low",
                "#F0AD4E"
            )

        return (
            "Too Low",
            "#D9534F"
        )



    # Oberhalb optimal

    if value > optimal_high:

        difference = value - optimal_high


        if difference <= tolerance:

            return (
                "Slightly High",
                "#F0AD4E"
            )

        return (
            "Too High",
            "#D9534F"
        )



def create_scale(
        parent,
        value,
        min_value,
        max_value,
        optimal
):


    canvas = ctk.CTkCanvas(
        parent,
        width=200,
        height=35,
        highlightthickness=0
    )

    canvas.pack(
        side="left",
        padx=10
    )


    width = 170
    x0 = 10
    y = 18



    def normalize(v):

        return (
            x0 +
            width *
            (
                (v - min_value)
                /
                (max_value - min_value)
            )
        )



    optimal_low, optimal_high = optimal


    tolerance = (
        max_value - min_value
    ) * 0.15



    # Positionen

    x_min = x0
    x_max = x0 + width


    x_opt_low = normalize(
        optimal_low
    )

    x_opt_high = normalize(
        optimal_high
    )


    x_slight_low = normalize(
        optimal_low - tolerance
    )


    x_slight_high = normalize(
        optimal_high + tolerance
    )


    # Begrenzen

    x_slight_low = max(
        x_min,
        x_slight_low
    )

    x_slight_high = min(
        x_max,
        x_slight_high
    )



    # -----------------------------------
    # Skalenbereiche
    # -----------------------------------

    # Too Low

    canvas.create_line(
        x_min,
        y,
        x_slight_low,
        y,
        width=8,
        fill="#D9534F"
    )


    # Slightly Low

    canvas.create_line(
        x_slight_low,
        y,
        x_opt_low,
        y,
        width=8,
        fill="#F0AD4E"
    )


    # Optimal

    canvas.create_line(
        x_opt_low,
        y,
        x_opt_high,
        y,
        width=8,
        fill="#5CB85C"
    )


    # Slightly High

    canvas.create_line(
        x_opt_high,
        y,
        x_slight_high,
        y,
        width=8,
        fill="#F0AD4E"
    )


    # Too High

    canvas.create_line(
        x_slight_high,
        y,
        x_max,
        y,
        width=8,
        fill="#D9534F"
    )



    # -----------------------------------
    # Marker
    # -----------------------------------

    position = normalize(
        max(
            min_value,
            min(
                max_value,
                value
            )
        )
    )


    canvas.create_oval(
        position - 6,
        y - 6,
        position + 6,
        y + 6,
        fill="black",
        outline="white",
        width=2
    )


    return canvas



def create_metric_row(
        parent,
        metric,
        metrics
):


    category = metric["category"]
    key = metric["key"]


    value = metrics[category][key]



    row = ctk.CTkFrame(
        parent
    )

    row.pack(
        fill="x",
        padx=10,
        pady=4
    )



    # Name

    ctk.CTkLabel(
        row,
        text=metric["title"],
        width=220,
        anchor="w"
    ).pack(
        side="left"
    )



    # Wert

    ctk.CTkLabel(
        row,
        text=f"{value:.2f}{metric['unit']}",
        width=100
    ).pack(
        side="left"
    )



    # Status

    status, color = get_status(
        value,
        metric["min"],
        metric["max"],
        metric["optimal"],
        metric.get(
            "direction",
            "range"
        )
    )


    ctk.CTkLabel(
        row,
        text=status,
        width=130,
        text_color=color,
        font=ctk.CTkFont(
            weight="bold"
        )
    ).pack(
        side="left"
    )



    # Skala

    if metric.get(
        "show_scale",
        False
    ):

        create_scale(
            row,
            value,
            metric["min"],
            metric["max"],
            metric["optimal"]
        )


    return row