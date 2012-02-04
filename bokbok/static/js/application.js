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

  function updateTarget(old, nnew) {
    pos = $.inArray(old, graphiteTargets)
    if (pos > -1) {
      graphiteTargets[pos] = nnew
      $('ul#graph-target-list>li').each(function(){
        var selector = $(this).find('span')
        if ($(selector).text() == old) {
          $(selector).text(nnew)
        }
      })

      updateGraph(graphiteTargets, graphiteOptions)
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

  $('li>a.close').live('click', function(){
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
  }).live('mouseenter', function(){
    $(this).tooltip('show')
  }).live('mouseleave', function(){
    $(this).tooltip('hide')
  })

  $('a#graph-share').live('mouseenter', function(){
    $(this).tooltip('show')
  }).live('mouseleave', function(){
    $(this).tooltip('hide')
  })

  $('a#graph-save').click(function(e){
    e.preventDefault()
    saveGraph(graphiteTargets, graphiteOptions, function(graphId){
      link = location.protocol + '//' + location.host + '/graph/view/' +
        graphId
      $('#graph-modal').find('input').val(link)
      $('#graph-modal').modal()
      $('#graph-modal').find('input').select()
    })
  }).live('mouseenter', function(){
    $(this).tooltip('show')
  }).live('mouseleave', function(){
    $(this).tooltip('hide')
  })

  $('a#graph-update').tooltip({
    title: 'Update the graph above.',
    placement: 'right'
  })

  $('a#graph-share').tooltip({
    title: 'Share this graph.',
    placement: 'right'
  })

  $('a#graph-save').tooltip({
    title: 'Take a snapshot of this graph image.',
    placement: 'right'
  })

  $('button.reset').tooltip({
    title: 'Reset the form below',
    placement: 'right'
  })

  $('i#search-help').tooltip({
    title: 'Search via substring and select the metric from the ' +
      'dropdown, or type a whole metric and press Enter to submit.',
    placement: 'right'
  })

  $('ul#graph-target-list').find('span').live('click', function(e){
    $('#graph-target-modal').find('input#graph-target').attr('data-target', $(this).text())
    $('#graph-target-modal').find('input#graph-target').val($(this).text())
    $('#graph-target-modal').modal()
  })

  $('#graph-target-modal').find('a.update').click(function(e){
    var old = $('#graph-target-modal').find('input#graph-target').attr('data-target'),
      nnew = $('#graph-target-modal').find('input#graph-target').val()
     updateTarget(old, nnew)
  })
})
