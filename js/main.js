const testChart = {
    "$schema": "https://vega.github.io/schema/vega-lite/v6.json",

    "description": "Test wildlife observation chart",

    "width": 600,
    "height": 350,

    "data": {
        "values": [
            {"species": "Kangaroo", "observations": 120},
            {"species": "Koala", "observations": 75},
            {"species": "Wombat", "observations": 55},
            {"species": "Echidna", "observations": 40},
            {"species": "Platypus", "observations": 30}
        ]
    },

    "mark": {
        "type": "bar",
        "cornerRadiusEnd": 5
    },

    "encoding": {

        "x": {
            "field": "species",
            "type": "nominal",
            "title": "Species"
        },

        "y": {
            "field": "observations",
            "type": "quantitative",
            "title": "Number of observations"
        },

        "tooltip": [
            {
                "field": "species",
                "type": "nominal",
                "title": "Species"
            },
            {
                "field": "observations",
                "type": "quantitative",
                "title": "Observations"
            }
        ]
    }
};

vegaEmbed("#test-chart", testChart, {
    actions: false
});