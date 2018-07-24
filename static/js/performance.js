$(document).ready(function() {
    $('#performance-link').addClass('active');
    
    // Win Perf
    window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";
        Plotly.plot(
            '3cfdfd73-3fcc-4767-a501-b70a3d06688a',
            [{"name": "BetSmart", "x": [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018], "y": [0.6804707933740192, 0.6957250628667225, 0.6886138613861386, 0.7069256756756757, 0.6972361809045227, 0.6908212560386473, 0.6934220830070478, 0.6861370716510904, 0.6957547169811321, 0.6985003946329913, 0.6724137931034483, 0.6858372456964006], "type": "bar", "uid": "c73222da-82bf-11e8-89eb-1a20ced466c5"}, {"name": "Naive", "x": [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018], "y": [0.6148705096073517, 0.6482558139534884, 0.6579563182527302, 0.64140625, 0.653755868544601, 0.6296829971181557, 0.64921875, 0.653069153069153, 0.6700626959247649, 0.6575875486381323, 0.6179467084639498, 0.6388888888888888], "type": "bar", "uid": "c7322780-82bf-11e8-89eb-1a20ced466c5"}],
            {"xaxis": {"title": "Season"}, "yaxis": {"range": [0.6048705096073517, 0.7169256756756757], "title": "Accuracy"}},
            {"showLink": false, "linkText": "Export to plot.ly"}
        ).then(function () {return Plotly.addFrames('3cfdfd73-3fcc-4767-a501-b70a3d06688a',{});}).then(function(){Plotly.animate('3cfdfd73-3fcc-4767-a501-b70a3d06688a');})
    window.addEventListener("resize", function(){Plotly.Plots.resize(document.getElementById("3cfdfd73-3fcc-4767-a501-b70a3d06688a"));});
    
    // Spread Perf
    window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";
        Plotly.plot(
            'b180427d-7f3d-426d-b69b-06c975ee8575',
            [{"name": "BetSmart", "x": [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018], "y": [0.5004420866489832, 0.48523206751054854, 0.5426579163248565, 0.5182333873581848, 0.5008445945945946, 0.5358527131782945, 0.5186360031720857, 0.4809825673534073, 0.5152610441767068, 0.5023980815347722, 0.5123015873015873, 0.5079872204472844], "type": "bar", "uid": "c7d1fb3e-82bf-11e8-89eb-1a20ced466c5"}, {"name": "Naive", "x": [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018], "y": [0.5037593984962406, 0.4754983388704319, 0.515600624024961, 0.512890625, 0.5160406885758998, 0.484149855907781, 0.476171875, 0.5143745143745144, 0.47962382445141066, 0.46731517509727627, 0.5007836990595611, 0.4956964006259781], "type": "bar", "uid": "c7d1ffa8-82bf-11e8-89eb-1a20ced466c5"}],
            {"xaxis": {"title": "Season"}, "yaxis": {"range": [0.45731517509727626, 0.5526579163248565], "title": "Accuracy"}},
            {"showLink": false, "linkText": "Export to plot.ly"}
        ).then(function () {return Plotly.addFrames('b180427d-7f3d-426d-b69b-06c975ee8575',{});}).then(function(){Plotly.animate('b180427d-7f3d-426d-b69b-06c975ee8575');})
    window.addEventListener("resize", function(){Plotly.Plots.resize(document.getElementById("b180427d-7f3d-426d-b69b-06c975ee8575"));});
    
    // Spread Profit
    window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";
        Plotly.plot(
            'ddac746a-d3c6-4a6b-bbcc-5427532b263a',
            [{"name": "BetSmart", "x": [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018], "y": [2.128375963199083, -5.432595706657854, 6.449756674916624, 2.335972551223329, 4.0503697175573776, 9.31133935029565, 3.010485252355285, 0.6023550511469445, 7.329252090077941, 3.1289335800797735, 5.0571334990293336, 4.0712828530309685], "type": "bar", "uid": "f88e1b60-82cc-11e8-89eb-1a20ced466c5"}],
            {"xaxis": {"title": "Season"}, "yaxis": {"range": [-6.432595706657854, 10.31133935029565], "title": "Profit (%)"}},
            {"showLink": false, "linkText": "Export to plot.ly"}
        ).then(function () {return Plotly.addFrames('ddac746a-d3c6-4a6b-bbcc-5427532b263a',{});}).then(function(){Plotly.animate('ddac746a-d3c6-4a6b-bbcc-5427532b263a');})
    window.addEventListener("resize", function(){Plotly.Plots.resize(document.getElementById("ddac746a-d3c6-4a6b-bbcc-5427532b263a"));});
    
    
    
    // Total Perf
    window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";
        Plotly.plot(
            'aedfae93-af5a-4dd5-93bf-de78005cf57d',
            [{"name": "BetSmart", "x": [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018], "y": [0.5209606986899563, 0.5317258883248731, 0.5008019246190858, 0.49959709911361805, 0.5270773046713518, 0.5029239766081871, 0.5223642172523961, 0.5032128514056224, 0.5107655502392344, 0.5154884829229547, 0.49840891010342087, 0.5419635787806809], "type": "bar", "uid": "c865d85e-82bf-11e8-89eb-1a20ced466c5"}, {"name": "Naive", "x": [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018], "y": [0.5129490392648287, 0.4742524916943522, 0.49453978159126366, 0.51328125, 0.5015649452269171, 0.5091258405379443, 0.48984375, 0.4996114996114996, 0.49059561128526646, 0.4910505836575875, 0.4898119122257053, 0.47730829420970267], "type": "bar", "uid": "c865dcaa-82bf-11e8-89eb-1a20ced466c5"}],
            {"xaxis": {"title": "Season"}, "yaxis": {"range": [0.4642524916943522, 0.5519635787806809], "title": "Accuracy"}},
            {"showLink": false, "linkText": "Export to plot.ly"}
        ).then(function () {return Plotly.addFrames('aedfae93-af5a-4dd5-93bf-de78005cf57d',{});}).then(function(){Plotly.animate('aedfae93-af5a-4dd5-93bf-de78005cf57d');})
    window.addEventListener("resize", function(){Plotly.Plots.resize(document.getElementById("aedfae93-af5a-4dd5-93bf-de78005cf57d"));});
})