var checkvalue;
$(document).ready(function()
{
    pwcheck();
    $("#passwordHelpBlock").hide();
    $("#login").submit(function(e)
    {
        if($("#psw").hasClass("togglevis"))
        {
            $("#passwordHelpBlock").show();
            e.preventDefault();
            return false;
        }
    });


    $("#psw").keyup(function()
    {
        pwcheck()
    });

});




function pwcheck()
{
    checkvalue = null;
    return $.getJSON("/pwcheck", {username: $("#usrn").val(), password: $("#psw").val()}, function(data)
    {
        if(!data.check)
        {
            $("#psw").addClass("togglevis");
        }
        else
        {
           $("#psw").removeClass("togglevis");
        }
    });
};
