/**
 * Created by tianpengqi on 2015/12/19.
 */
$(function(){
    $(document).on('click', '.submitBtn', function(){
        var jsonText = $('.jsonText:eq(0)').val();
        var type = $('#serializeType option:selected').val();
        if(jsonText!='' && jsonText!=null){
            $.ajax({
                type: 'POST',
                url: '/prettyJson',
                data: {jsonText: jsonText, type: type },
                success: function (msg) {
                    $('#jsonContent').text(msg);
                },
                error:function(){

                }
            });
        }
    });
    $(document).on('click', '#toTimeBtn', function(){
        var _this = $(this);
        var time = _this.prev().val();
        console.log(time);
        if(time!=''){
            $.ajax({
                type: 'POST',
                url: 'time-parse',
                data: { time: time, type:'toDate' },
                success: function(msg){
                    _this.parent().children().last().val(msg);
                }
            });
        }
    });
    $(document).on('click', '#toTimestampBtn', function(){
        console.log(1)
        var _this = $(this);
        var dateTime = _this.prev().prev().val();
        if(dateTime!=''){
            $.ajax({
                type: 'POST',
                url: 'time-parse',
                data: { date_time: dateTime, type:'toTimestamp' },
                success: function(msg){
                    if(msg!='error'){
                        _this.parent().children().last().val(msg);
                    }else{
                        alert('日期格式不对');
                    }

                }
            });
        }
    });
    $(document).on('click', '#httpStart', function(){
        var start = $(this).text();
        if(start=='http://'){
            $(this).text('https://');
        }else{
            $(this).text('http://');
        }
    });
    $(document).on('click', '.paramsDelBtn', function(){
        $(this).parent().remove();
    });
    $('#addPramsBtn').click(function(){
        var paramsContainer = $('#paramsContainer');
        var len = paramsContainer.find('div').length;
        var text = $('.paramsLabel:eq('+(len-1)+')').text();
        var h = text.substr(2);
        len = parseInt(h);
        var html = '<div class="from-group form-inline col-sm-12" style="padding-top: 9px"> ' +
            '<label class="control-label col-sm-2 paramsLabel">参数'+(len+1)+'</label> ' +
            '<input class="form-control attribute"  placeholder="参数名" name="attribute_'+(len+1)+'" type="text" value=""> ' +
            '<input class="form-control value" placeholder="参数值" name="value_'+(len+1)+'" type="text" value=""> ' +
            '<button class="form-control btn-warning paramsDelBtn">删除</button>' +
            ' </div>';
        paramsContainer.append(html);
    });
    $('#addHeaderBtn').click(function(){
        $('#headerDefine').toggle();
    });
    $('#getRequestBtn').click(function(){
        fetchRequest('GET');
    });
    $('#postRequestBtn').click(function(){
        fetchRequest('POST');
    });
})

function toggleBtn(obj){
    $(obj).prev().toggle();
    $(obj).prev().prev().toggle();
}

function fetchRequest(type){
    var httpStart = $('#endPoint').prev().text();
        var endPoint = $('#endPoint').val();
        var data = {};
        if(endPoint!=''){
            data.endpoint = httpStart+endPoint;
            var header = $(':text[name="header"]:eq(0)').val();
            if(header!=''){
                data.header = header;
            }
            data.type = type;
            var params = new Array();
            $('.attribute').each(function(){
                if($(this).val()!=''){
                    params[$(this).val()] = $(':text[name="'+$(this).attr('name').replace('attribute', 'value')+'"]:eq(0)').val();
                }
            });
            if(params.length!=0){
                data.params = params;
            }
            console.log(params);
            $.ajax({
                type: 'POST',
                url: '/fetch-request',
                data: data,
                success: function(msg){
                    console.log(msg);
                    $('#response').text(msg);
                }
            });
        }
}