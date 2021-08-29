$(document).ready(function()
{
    // first_name validation
    $('#searchMarket').keyup(function()
    {
        var data = $("#searchForm").serialize()   
        $.ajax
        ({
            method: "POST",   
            url: "/market/search/ajax",
            data: data
        })
        .done(function(response)
        {
            $('#market_table').html(response);
            $('#main_heading').replaceWith("<h3>Your Search results:</h3>");
        })
        return false
    })
})

