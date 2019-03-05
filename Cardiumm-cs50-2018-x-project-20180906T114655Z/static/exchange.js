$(document).ready(function()
{
    // $('#firstcurrency').empty();

    balcheck();
    $("#exchange").click(function(){
            $('#exchange').attr("disabled", true);
            console.log("clicked")
            firstcurrency= $("#firstcurrency option:selected" ).text().trim()
            secondcurrency= $("#secondcurrency option:selected" ).text().trim()
            amount= $("#currency2value").val()
            exchanged= $("#currency1value").val()
            console.log("ALL GOOD")
            value= fx.convert(1, {from:secondcurrency , to: "TRY"})
            firstvalue = fx.convert(1, {from:firstcurrency , to: "TRY"})
            cost= value * amount
        if($("#currency1value").hasClass("is-invalid") == false)
        {
        $.post( "/exchange", {
            firstcurrency: firstcurrency,
            firstvalue: firstvalue,
            secondcurrency: secondcurrency,
            amount: amount,
            exchanged: exchanged,
            value: value,
            cost: cost
        },
        function( data ) {
            alert("Exchanged "+data.Exchanged+ " with total value of "+Number.parseFloat(data.Value).toFixed(3)+"TRY for "+Number.parseFloat(data.Amount).toFixed(3)+" "+data.Currency)
            balcheck();
            $('#exchange').attr("disabled", false);
        }, "json");
        }
    });

    $.getJSON(
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
        amountinfo();
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
    amount = $("#firstcurrency option:selected" ).val();
    console.log(firstamount)
    var counter = 0;
    var dotcounter =0;
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
    if (parseFloat(amount) < parseFloat(firstamount) && counter == 0)
    {
        $("#currency1value").addClass("is-invalid").removeClass("is-valid");
        $("#errorblock").html(`<font color="red">You currently don't have enough for this transaction.</font>`);
    }
    if (counter == 0)
    {
        if (parseFloat(amount) >= parseFloat(firstamount))
        {
            $("#currency1value").addClass("is-valid").removeClass("is-invalid");
            $("#errorblock").html(``);
        }
        // var secondamount = $("#currency2value").val();
        var firstcurrency = $("#firstcurrency option:selected" ).text().trim();
        var secondcurrency = $("#secondcurrency option:selected" ).text().trim();
        var secondamount = fx.convert(firstamount, {from: firstcurrency, to: secondcurrency});
        secondamount = Number.parseFloat(secondamount).toFixed(3);
        $('#currency2value').val(secondamount);
        // console.log(fx.convert(1, {from: "USD", to: "TRY"}));
    }

}

function amountinfo()
{
    selected = $("#firstcurrency option:selected" ).text();
    amount = $("#firstcurrency option:selected" ).val();
    if(amount != 0)
    {
        $("#exchangeBlock").html(`You currently have ${amount} ${selected} .`);
    }
}

function balcheck()
{
    $.post( "/checkbal",
    function( data ) {
        $('#firstcurrency').empty();
        data = data.rowlist;
        for(i=0; i < data.length; i++)
        {
            if(data[i].amount > 0)
            {
                $("#firstcurrency").append('<option value="'+data[i].amount+'">'+data[i].acronym+'</option>');
            }

        }
        amountinfo();
    }, "json");
}