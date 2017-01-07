var recordingId = null;
var graph = null;

function initDygraph(id, data) {
    recordingId = id;
    graph = new Dygraph(
        document.getElementById("graph"),
        data,
        {
            // options go here. See http://dygraphs.com/options.html
            legend: 'always',
            animatedZooms: true,
            title: 'ECG chart'
        });
}

function changeData(startTime, endTime) {
    var getRecordingUrl = "/recordings/" + recordingId + "?from=" + startTime + "&to=" + endTime;
    $.get(getRecordingUrl, function(response) {
        graph.updateOptions({ file: response.recordingData });
    });
}

function initClickOnDurationPickers() {
    $("#change-time-range-button").click(function() {
        var startTime = $("#start-time-picker").val();
        var endTime = $("#end-time-picker").val();
        changeData(startTime, endTime);
    });
}
