$(function(){
  var graphiteOptions = {},
    graphiteTargets = []

  function addTarget(target) {
    if ($.inArray(target, graphiteTargets) == -1) {
        graphiteTargets.push(target)
        $('ul#graph-target-list').append('<li><a class="close">&times;</a><span class="editable">'+target+'</span></li>')
        updateGraph(graphiteTargets, graphiteOptions)
        $('ul#graph-target-list>li').each(function(){
          if ($(this).find('span').text() === target) {
            $(this).data('current', target)
          }
        })
        $('input#metrics-select').val('')
    }
  }

  function updateTarget(previous, current) {
    pos = $.inArray(previous, graphiteTargets)
    if (pos > -1) {
      graphiteTargets[pos] = current
      $('ul#graph-target-list>li').each(function(){
        if ($(this).data('current') === previous) {
          $(this).data('current', current)
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

  $('#graph-target-list').find('.editable').live('mouseover', function(){
    if (!$(this).data('init')) {
      $(this).data('init', true)
      $(this).editable(function(current, settings){
        var previous = $(this).parent().data('current')
        updateTarget(previous, current)
        return(current)
      }, {
        indicator: '',
        type: 'text'
      })
    }
  })
})
