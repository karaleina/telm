var recordingId = null;
var graph = null;

function initDygraph(id, data, labels) {
    recordingId = id;
    graph = new Dygraph(
        document.getElementById("graph"),
        data,
        {
            labels: ["Time", "Plot1", "Plot2"],
            legend: 'always',
            animatedZooms: true,
            title: 'ECG chart'
        });
    graph.setAnnotations(qrsLabelsToAnnotations(labels));
}

function qrsLabelsToAnnotations(qrsLabels) {
    var annotations = [];
    for (var i = 0; i < qrsLabels.length; i++) {
        var qrsLabel = qrsLabels[i];
        annotations.push({
            series: "Plot" + (qrsLabel.plotId + 1),
            x: qrsLabel.time,
            tickHeight: 4,
            width: 20,
            height: 20,
            shortText: qrsLabel.type,
            text: "załamek " + qrsLabel.type
        });
    }
    return annotations;
}

function changeData(startTime, endTime) {
    var getRecordingUrl = "/recordings/" + recordingId + "?from=" + startTime + "&to=" + endTime;
    $.get(getRecordingUrl, function(response) {
        graph.updateOptions({ file: response.recordingData });
        graph.setAnnotations(qrsLabelsToAnnotations(response.labels));
        console.log(response);
        for (var plotId = 0; plotId < response.RR_means.length; plotId++) {
	        var mean_rr_info_for_plot = response.RR_means[plotId];
	        var mean_distance = mean_rr_info_for_plot['distance'];
	        var mean_frequency = mean_rr_info_for_plot['frequency'];
	        var diagnosis = mean_rr_info_for_plot['diagnosis'];

	        $("#rr_means_distance_" + plotId).html(mean_distance);
	        $("#rr_means_frequency_" + plotId).html(mean_frequency);
	        $("#rr_means_diagnosis_" + plotId).html(diagnosis);
        }
    });
}



function initClickOnDurationPickers() {
    $("#change-time-range-button").click(function() {
        var startTime = $("#start-time-picker").val();
        var endTime = $("#end-time-picker").val();
        changeData(startTime, endTime);
    });
}
