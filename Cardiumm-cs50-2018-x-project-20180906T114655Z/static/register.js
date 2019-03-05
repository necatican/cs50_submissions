$(document).ready(function()
{
    $("#secrets").hide();


    $("#register").submit(function(e){
    $('#exchange').attr("disabled", true);
        if($("#usr").hasClass("is-invalid") || $("#pw").hasClass("is-invalid") || $("#pwc").hasClass("is-invalid"))
        {
            e.preventDefault();
            $('#exchange').attr("disabled", false);
            return false;

        }
    }
    );


    $("#accept").change(function()
    {
        var checkboxvalue = $("#accept").is(":checked");
        if(checkboxvalue)
        {
            $("#secrets").show();
            $("#secretkey").prop('required',true);
            $("#secret").prop('required',true);
        }
        else
        {
            $("#secrets").hide();
            $("#secretkey").prop('required',false);
            $("#secret").prop('required',false);
        }
    })
    $("#usr").keyup( function()
    {  if($("#usr").val().length > 4)
    {
        checkusr();
    }
    else{
        $("#usr").addClass("is-invalid").removeClass("is-valid");}
        $("#existingpw").html(``);
    });

    $("#pw").keyup( function()
    {
        checkpwc();
        pswd = $("#pw").val();
        var numeral_count = 0;
        var capitalized_count = 0;
        if(pswd.length > 7)
        {

            for (var i=0; i < pswd.length; i++)
            {
                if ('0123456789'.indexOf(pswd.charAt(i)) !== -1)
                {
                    numeral_count++;
                }
                else if(pswd.charAt(i) == pswd.charAt(i).toUpperCase())
                {
                    capitalized_count++;
                }

                if (numeral_count > 0 && capitalized_count > 0)
                {
                    $("#pw").removeClass("is-invalid").addClass("is-valid");
                }
                else
                {
                    $("#pw").removeClass("is-valid").addClass("is-invalid");
                }
            }

        }
        else
        {
            $("#pw").removeClass("is-valid").addClass("is-invalid");
        }

    });

    $("#pwc").keyup( function()
    {
        checkpwc();
    });
});




function checkusr()
{
    $.getJSON("/checkusr", {username: $("#usr").val()}, function(data)
    {
        if (data.count != 0)
        {
            $("#errorblock").html(`<font color="red">${data.username} already exists in our database</font>`);
            $("#passwordHelpBlock").removeClass("togglevis");
            $("#usr").addClass("is-invalid").removeClass("is-valid");
        }
        else
        {
            $("#usr").removeClass("is-invalid").addClass("is-valid");
            $("#errorblock").html(``);
        }
    });
}

function checkpwc()
{
    pw = $("#pw").val();
    pwc = $("#pwc").val();
    if(pw == pwc)
    {
        $("#pwc").removeClass("is-invalid").addClass("is-valid");
    }
    else
    {
        $("#pwc").removeClass("is-valid").addClass("is-invalid");
    }
}

