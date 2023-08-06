save_calibration module
=======================

.. automodule:: save_calibration
   :members:
   :undoc-members:
   :show-inheritance:


Calibration file format
-----------------------
Example of a calibrated tagger entry in a calibration file

.. code-block:: python

    "OSmu": {
        "PolynomialCalibration": {  # Calibration function class
            "degree": "1",          # Polynomial degree (number of params per flavour - 1)
            "link": "mistag"        # Type of mistag
        },
        "osc": {  # Oscillation parameters used in calibration
            "DeltaM": null,
            "DeltaGamma": null,
            "Aprod": "0"
        },
        "calibration": {
            "avg_eta": "0.3377155702903403",  # Average uncalibrated mistag
            "flavour_style": {                # Parameters in the form of p+ and p- parameters
                "params": {                   # Calibration parameters with uncertainties
                    "p0+": [
                        "-0.008027361478473534",
                        "0.008103797683204187"
                    ],
                    "p1+": [
                        "1.189111350849578",
                        "0.12629576532833553"
                    ],
                    "p0-": [
                        "-0.007600434798924063",
                        "0.00803168577147565"
                    ],
                    "p1-": [
                        "1.3357207683763836",
                        "0.12066342352175546"
                    ]
                },
                "cov": [ # Parameter covariances matrix with parameters in same order as given under params (row, by row)
                    [
                        "6.567153689030556e-05",
                        "0.00010315418880612141",
                        "9.833488959912964e-15",
                        "9.302766371735791e-13"
                    ],
                    [
                        "0.00010315418880612141",
                        "0.015950620339870002",
                        "1.5446045955771038e-14",
                        "1.46124084218125e-12"
                    ],
                    [
                        "9.833488959912964e-15",
                        "1.5446045955771038e-14",
                        "6.450797633172438e-05",
                        "0.000153902901151279"
                    ],
                    [
                        "9.302766371735791e-13",
                        "1.46124084218125e-12",
                        "0.000153902901151279",
                        "0.014559661775990529"
                    ]
                ]
            },
            "delta_style": {    # Parameters in the form of p_i and Delta p_i parameters
                "params": {     # Calibration parameters with uncertainties
                    "p0": [
                        "-0.007813898138698799",
                        "0.005704811855830499"
                    ],
                    "p1": [
                        "2.2624160596129808",
                        "0.08733596355279853"
                    ],
                    "Dp0": [
                        "-0.00042692667954947073",
                        "0.011409623709937282"
                    ],
                    "Dp1": [
                        "-0.14660941752680556",
                        "0.17467192708886578"
                    ]
                },
                "cov": [  # Parameter covariance matrix with parameters in same order as given under params (row, by row)
                    [
                        "3.2544878310424226e-05",
                        "6.426427272578078e-05",
                        "5.817802792905884e-07",
                        "-2.5374356629994095e-05"
                    ],
                    [
                        "6.426427272578078e-05",
                        "0.007627570529695753",
                        "-2.5374355715163513e-05",
                        "0.0006954792819397369"
                    ],
                    [
                        "5.817802792905884e-07",
                        "-2.5374355715163506e-05",
                        "0.00013017951320236297",
                        "0.00025705708901167774"
                    ],
                    [
                        "-2.537435662999409e-05",
                        "0.0006954792819397369",
                        "0.00025705708901167774",
                        "0.030510282112938047"
                    ]
                ]
            }
        },
        "stats": {                # Event statistics without selection
            "N": "100000",        # Total number of events in sample
            "Nt": "6585",         # Total number of tagged events in sample
            "Neff": "100000.0",   # Effective number of total events
            "Nw": "100000.0",     # Weighted number of events
            "Nwt": "6585.0"       # Weighted number of tagged events
        },
        "selected_stats": {       # Event statistics with selection      
            "Ns": "100000",       # Total number of events in sample
            "Nts": "6585",        # Total number of tagged events in sample
            "Neffs": "100000.0",  # Effective number of total events
            "Nws": "100000.0",    # Weighted number of events
            "Nwts": "6585.0"      # Weighted number of tagged events
        },
        "uncalibrated": {   # Tagger performances before calibration
            "selected": {   # Tagger performances on selected events
                "tag_efficiency": [
                    "0.06585",
                    "0.0007843071942804043"
                ],
                "tag_power": [
                    "0.00800782064870546",
                    "9.537724138628498e-05"
                ]
            },
            "all": {    # Tagger performances on all events in sample
                "tag_efficiency": [
                    "0.06585",
                    "0.0007843071942804043"
                ],
                "tag_power": [
                    "0.00800782064870546",
                    "9.537724138628498e-05"
                ]
            }
        },
        "calibrated": {               # Tagger performances after calibration
            "selected": {             # Tagger performances on selected events
                "Nts": "6538",        # Selected number of tagged events (calibrated)
                "Nwts": "6538.0",     # Selected number of tagged events (calibrated + weighted)
                "tag_efficiency": [
                    "0.06538",
                    "0.0007816997863630255"
                ],
                "tag_power": [
                    "0.009343797506981482",
                    "0.0005968207955739008"
                ]
            },
            "all": {
                "Nt": "6538",       # Total number of tagged events (calibrated)
                "Nwt": "6538.0",    # Total number of tagged events (calibrated + weighted)
                "tag_efficiency": [
                    "0.06538",
                    "0.0007816997863630255"
                ],
                "tag_power": [
                    "0.009343797506981482",
                    "0.0005968207955739008"
                ]
            }
        }
    }
