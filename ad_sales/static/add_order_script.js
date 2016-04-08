function sel(input)
{
    if (input == 1)
    {
        document.getElementById("inp").style.display = "block";
        document.getElementById("upl").style.display = "none";
    }
    else
    {
        document.getElementById("inp").style.display = "none";
        document.getElementById("upl").style.display = "block";
    }
}