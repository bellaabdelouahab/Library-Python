{/* <tr >
<td>{{ result[1] }}</td>
<td>{{ result[2] }}</td>
<td>{{ result[3] }}</td>
<td>
    <form action="/ToReserve" method="post" name="Cancelation" style="display:inline" >
        <input type="text" style="display: none;" name="Cancelation_i" value={{result[1]}}>
        <input type="submit" name="testing" value="Cancel">
    </form>
    <form action="/ToReserve" method="post" name="Validation" style="display:inline">
        <input type="text" style="display: none;" name="Validation_i" value={{result[1]}}>
        <input type="submit" value="Reserve">
    </form>
</td>
</tr> */
}
// console.log(Data);
let DataCounter = 0;
$(".nextbtn").click(function(){
    if(DataCounter>Data.length-20){
        return
    }
    const Table = document.getElementsByClassName("tableData")[0]
    //Clear The table form data
    var TableData=document.querySelectorAll(".Data")
    while(TableData.length>0){
        try {
            Table.removeChild(document.querySelectorAll(".Data")[0])
        } catch (error) {
            break
        }
        
    }
    
    // Fill in the new data
    for (var counter = DataCounter; counter < DataCounter+20; counter++) {
        FillinData(counter, Table);
    }
    DataCounter+=20
})
$(".prevbtn").click(function(){
    if(DataCounter<20){
        return;
    }
    const Table = document.getElementsByClassName("tableData")[0]
    //Clear The table form data
    var TableData=document.querySelectorAll(".Data")
    while(TableData.length>0){
        try {
            Table.removeChild(document.querySelectorAll(".Data")[0])
        } catch (error) {
            break
        }
    }
    // Fill in the new data
    for (var counter = DataCounter-20; counter < DataCounter; counter++) {
        FillinData(counter, Table);
    }
    
    DataCounter-=20
})
let Elem = document.getElementsByClassName("Elem")[0]
Elem.innerHTML =DataCounter+"-"+(DataCounter+20)+"/"+Object.keys(Data).length;

function FillinData(counter, Table) {
    var Tr = document.createElement("TR");
    Tr.setAttribute("class", "Data");
    var Tdlist = [];
    for (var i = 1; i < Data[counter].length; i++) {
        var td = document.createElement("TD");
        td.innerHTML = Data[counter][i];
        Tdlist.push(td);
    }
    var td = document.createElement("TD");
    td.innerHTML = '<form action="/ToReserve" method="post" name="Cancelation" style="display:inline" ><input type="text" style="display: none;" name="Cancelation_i" value={{result[1]}}><input type="submit" name="testing" value="Cancel"></form><form action="/ToReserve" method="post" name="Validation" style="display:inline"><input type="text" style="display: none;" name="Validation_i" value={{result[1]}}><input type="submit" value="Reserve"></form>';
    Tdlist.push(td);
    for (var i = 0; i < Tdlist.length; i++) {
        Tr.appendChild(Tdlist[i]);
    }
    Table.appendChild(Tr);
}
$(".nextbtn").fire()
//fire a button action


