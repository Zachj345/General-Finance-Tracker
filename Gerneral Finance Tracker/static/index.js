// adding a new expense button  (js version)




function removeExpense(id) {
    let table = document.getElementById('expense-table');

    fetch(`/remove/${id}`, {method:'POST'}).then((res) => res.json()).then((data) => {
        console.log(data)
        $(table).load(document.URL + ' ' + '#expense-table ');
     
    })
    .catch((e) => alert(e))
    return false;
};

function filterByAmount() {
    let defaultRow = document.querySelectorAll('.default-row');
    let amountRow = document.querySelectorAll('.amount-row');
    let dateRow = document.querySelectorAll('.date-row');
    let categoryRow = document.querySelectorAll('.category-row');
    
   

    defaultRow.forEach(row => row.classList.add('hide'));
    categoryRow.forEach(row => row.classList.add('hide'));
    dateRow.forEach(row => row.classList.add('hide'));
    amountRow.forEach(row => row.classList.remove('hide'));

    return false;
};

function filterByCategory() {
    let defaultRow = document.querySelectorAll('.default-row');
    let amountRow = document.querySelectorAll('.amount-row');
    let dateRow = document.querySelectorAll('.date-row');
    let categoryRow = document.querySelectorAll('.category-row');
    
   
    amountRow.forEach(row => row.classList.add('hide'));
    defaultRow.forEach(row => row.classList.add('hide'));
    dateRow.forEach(row => row.classList.add('hide'));
    categoryRow.forEach(row => row.classList.remove('hide'));
    

    return false;
}

function filterByDate() {
    let defaultRow = document.querySelectorAll('.default-row');
    let amountRow = document.querySelectorAll('.amount-row');
    let dateRow = document.querySelectorAll('.date-row');
    let categoryRow = document.querySelectorAll('.category-row');
    
    categoryRow.forEach(row => row.classList.add('hide'));
    amountRow.forEach(row => row.classList.add('hide'));
    defaultRow.forEach(row => row.classList.add('hide'));
    dateRow.forEach(row => row.classList.remove('hide'));
    
    return false;

};