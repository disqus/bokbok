  function Graph(host, options) {
    this.graphiteHost = host
    this.options = options
    this.targets = []

    var self = this

    this.permalink = function(callback) {
      var config = {
        targets: self.targets,
        options: self.options
      }

      $.post('/graph', {config: JSON.stringify(config)}, function(data) {
        callback(data.message)
      })
    }

    this.snapshot = function(callback) {
      $.post('/graph/snapshot', {url: self.url()}, function(data){
        callback(data.message)
      })
    }

    this.update = function() {
      $('#graphite-img').attr('src', self.url())
    }

    this.url = function() {
      var url = 'http://'+self.graphiteHost+'/render?'

      for (var i = 0; i < self.targets.length; i++)
        url += '&target=' + self.targets[i]

      for (var k in self.options) {
        if (self.options.hasOwnProperty(k))
          url += '&' + k + '=' + encodeURIComponent(self.options[k])
      }

      return(url)
    }
  }

$(function(){
  function addTarget(target) {
    if ($.inArray(target, graph.targets) == -1) {
        graph.targets.push(target)
        $('ul#graph-target-list').append('<li><a class="close">&times;</a><span class="editable">'+target+'</span></li>')
        graph.update()
        $('ul#graph-target-list>li').each(function(){
          if ($(this).find('span').text() === target) {
            $(this).data('current', target)
          }
        })
        $('input#metrics-select').val('')
    }
  }

  function updateTarget(previous, current) {
    pos = $.inArray(previous, graph.targets)
    if (pos > -1) {
      graph.targets[pos] = current
      $('ul#graph-target-list>li').each(function(){
        if ($(this).data('current') === previous) {
          $(this).data('current', current)
        }
      })

      graph.update()
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
  }).click(function(){
    $('i#search-help').popover('hide')
    $.cookie('visited', true)
  })

  $('li>a.close').live('click', function(){
    var parent = $(this).closest('li'),
      metric,
      idx

    metric = parent.children('span').text()
    var idx = graph.targets.indexOf(metric)
    if (idx != -1) {
      graph.targets.splice(idx, 1)
      parent.remove()
      graph.update()
    }
  })

  $('a#graph-update').click(function(e){
    e.preventDefault()
    $.each($('#graph-form').serializeArray(), function(i, field) {
      if (field.value.length > 0)
        graph.options[field.name] = field.value
    })
    graph.update()
  }).live('mouseenter', function(){
    $(this).tooltip('show')
  }).live('mouseleave', function(){
    $(this).tooltip('hide')
  })

  $('a#graph-permalink').click(function(e) {
    e.preventDefault()
    graph.permalink(function(graphId) {
      link = location.protocol + '//' + location.host + '/graph/' +
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

  $('a#graph-snapshot').click(function(e){
    e.preventDefault()
    graph.snapshot(function(graphId){
      link = location.protocol + '//' + location.host + '/graph/snapshot/' +
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

  $('a#graph-permalink').tooltip({
    title: 'Share this graph.',
    placement: 'right'
  })

  $('a#graph-snapshot').tooltip({
    title: 'Take a snapshot of this graph image.',
    placement: 'right'
  })

  $('button.reset').tooltip({
    title: 'Reset the options below',
    placement: 'right'
  })

  $('i#search-help').popover({
    title: 'Hello!',
    content: 'Search via substring and select the metric from the ' +
      'dropdown, or type a whole metric and press Enter to submit.',
    placement: 'right',
    trigger: 'manual'
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

  if (!$.cookie('visited')) {
    setTimeout(function(){
      $('i#search-help').popover('show')
      },
   50)
  }
})
