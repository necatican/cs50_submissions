$(document).ready(function()
{

    $("#addfunds").click(function(){
        console.log("clicked")
        $.post( "/addfunds", { firstcurrency: $("#firstcurrency").val(), amount: $("#currency1value").val() },
        function( data ) {
            alert("Added " + data.Amount+ " " + data.Currency+" ( "+data.Value+" TRY)")
        }, "json");
    });

    $.getJSON(
    // NB: using Open Exchange Rates here, but you can use any source!
    'http://openexchangerates.org/api/latest.json?app_id=407d8ce1d4294f86ba0c5d82037a307c', function(data) {
    // Check money.js has finished loading:
    if (typeof fx !== "undefined" && fx.rates) {
        fx.rates = data.rates;
        fx.base = data.base;
    } else {
        // If not, apply to fxSetup global:
        var fxSetup = {
            rates: data.rates,
            base: data.base
        };
    }

     $("#firstcurrency").change(function()
    {
        checkval();
    });
    $("#secondcurrency").change(function()
    {
        checkval();
    });
    $("#currency1value").keyup(function()
    {
        checkval();
    });

  });

});

function checkval()
{
    var firstamount = $("#currency1value").val();
    var counter = 0;
    var dotcounter = 0;
    for (var i=0; i < firstamount.length; i++)
    {
        if ('0123456789.'.indexOf(firstamount.charAt(i)) == -1)
        {
            $("#currency1value").addClass("is-invalid").removeClass("is-valid");
            $('#currency2value').val("INVALID VALUE");
            counter++;
        }
        else if ('.'.indexOf(firstamount.charAt(i)) == 0)
        {
            dotcounter++;
            if (dotcounter > 1)
            {
                $("#currency1value").addClass("is-invalid").removeClass("is-valid");
                $('#currency2value').val("INVALID VALUE");
                counter++;
            }
        }
    }

    if (counter == 0)
    {
        $("#currency1value").addClass("is-valid").removeClass("is-invalid");
        // var secondamount = $("#currency2value").val();
        var firstcurrency = $("#firstcurrency").val();
        var secondcurrency = $("#secondcurrency").val();
        var secondamount = fx.convert(firstamount, {from: firstcurrency, to: secondcurrency});
        secondamount = Number.parseFloat(secondamount).toFixed(2)
        $('#currency2value').val(secondamount);
        // console.log(fx.convert(1, {from: "USD", to: "TRY"}));
    }

}