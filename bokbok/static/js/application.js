$(function(){
  var graphiteOptions = {},
    graphiteTargets = []

  function addTarget(target) {
    if ($.inArray(target, graphiteTargets) == -1) {
        graphiteTargets.push(target)
        $('ul#graph-target-list').append('<li><a class="close">&times;</a><span>'+target+'</span></li>')
        updateGraph(graphiteTargets, graphiteOptions)
        $('input#metrics-select').val('')
    }
  }

  function metricList(query) {
    var metricList = []

    jQuery.ajaxSetup({async:false});
    $.getJSON('/metrics.json?query=' + query, function(data) {
      metricList = data.message
    })
    jQuery.ajaxSetup({async:true});
    return(metricList)
  }

  $('.accordion').collapse()

  $('input#metrics-select').typeahead({
    source: metricList,
    onSelect: function(data){
      addTarget(data)
    }
  }).bind('keydown', function(e){
     var code = e.keyCode || e.which
     if (code == 13) {
       addTarget($(this).val())
     }
  })

  $('a.close').live('click', function(){
    var parent = $(this).closest('li'),
      metric,
      idx

    metric = parent.children('span').text()
    var idx = graphiteTargets.indexOf(metric)
    if (idx != -1) {
      graphiteTargets.splice(idx, 1)
      parent.remove()
      updateGraph(graphiteTargets, graphiteOptions)
    }
  })

  $('a#graph-update').click(function(e){
    e.preventDefault()
    $.each($('#graph-form').serializeArray(), function(i, field) {
      if (field.value.length > 0)
        graphiteOptions[field.name] = field.value
    })
    updateGraph(graphiteTargets, graphiteOptions)
  })

  $('a#graph-save').click(function(e){
    e.preventDefault()
    saveGraph(graphiteTargets, graphiteOptions, function(graphId){
      link = location.protocol + '//' + location.host + '/graph/view/' +
        graphId
      $('.modal-body>p>input').val(link)
      $('#graph-modal').modal()
    })
  })
    
  $('i#search-help').tooltip({
    title: 'Search via substring and select the metric from the ' +
      'dropdown, or type a whole metric and press Enter to submit it.',
    placement: 'right'
  })
})
