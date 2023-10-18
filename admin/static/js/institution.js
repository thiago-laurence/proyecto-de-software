// see how to use at the end of the script
const domParser = new DOMParser();
const dataList = {
    el:document.querySelector('.data-list'),
    listEl:document.querySelector('.option-list'),
    arrow:document.querySelector(".searchable-list>svg"),
    currentValue:null,
    listOpened :false,
    optionTemplate:
    `
    <li
        class='data-option select-none break-words inline-block text-sm text-gray-500 bg-gray-100 odd:bg-gray-200 hover:bg-gray-300 hover:text-gray-700 transition-all duration-200 font-bold p-3 cursor-pointer max-w-full '>
            [[REPLACEMENT]]
    </li>
    `,
    optionElements:[],
    options:[], 
    find(str){
        for(let i = 0;i<dataList.options.length;i++){
            const option = dataList.options[i];
            if(!option.toLowerCase().includes(str.toLowerCase())){
                dataList.optionElements[i].classList.remove('block');
                dataList.optionElements[i].classList.add('hidden');
            }else{
                dataList.optionElements[i].classList.remove('hidden');
                dataList.optionElements[i].classList.add('block');
            }
        }
    },  
    remove(value){
        const foundIndex = dataList.options.findIndex(v=>v===value);
        if(foundIndex!==-1){
            dataList.listEl.removeChild(dataList.optionElements[foundIndex])
            dataList.optionElements.splice(foundIndex,1);
            dataList.options.splice(value,1);
        }
    },
    append(value){    
        if(!value || typeof value === 'object' || typeof value === 'symbol' || typeof value ==='function') return;
        value = value.toString().trim();
        if(value.length === 0) return; 
        if(dataList.options.includes(value)) return;

        const html = dataList.optionTemplate.replace('[[REPLACEMENT]]',value);
        const targetEle = domParser.parseFromString(html, "text/html").querySelector('li');
        targetEle.innerHTML = targetEle.innerHTML.trim();
        dataList.listEl.appendChild(targetEle);
        dataList.optionElements.push(targetEle);  
        dataList.options.push(value);

        if(!dataList.currentValue) dataList.setValue(value);

        targetEle.onmousedown = (e)=>{
            dataList.optionElements.forEach((el,index)=>{
                if(e.target===el){
                    dataList.setValue(dataList.options[index]);
                    dataList.hideList();
                    return;
                }
            })
        }
    },  
    setValue(value){
        dataList.el.value = value;
        dataList.currentValue = value;
    },
    showList(){
        dataList.listOpened = true;
        dataList.listEl.classList.add('opacity-100');
        dataList.listEl.classList.add('scale-100');
        dataList.arrow.classList.add("rotate-0");
    },
    hideList(){
        dataList.listOpened = false;
        dataList.listEl.classList.remove('opacity-100');
        dataList.listEl.classList.remove('scale-100');
        dataList.arrow.classList.remove("rotate-0");
    },
    init(){ 
        dataList.arrow.onclick = ()=>{
            dataList.listOpened ? dataList.hideList(): dataList.showList();
        } 
        dataList.el.oninput = (e)=>{
            dataList.find(e.target.value);
        }
        dataList.el.onclick= (el)=>{
            dataList.showList();
            for(let el of dataList.optionElements){
                el.classList.remove('hidden');
            }
        }
        dataList.el.onblur = (e)=>{
            dataList.hideList();
            dataList.setValue(dataList.currentValue);
        }
    }
}

// how to use
dataList.init(); 
// add items
let url = "/users/all-users"
const data = fetch(url, {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json'
    }
}).then(response => response.json())
.then(data => {
    data.forEach(v=>(dataList.append(v))); 
});
//data.forEach(v=>(dataList.append(v))); 

// remove item
// dataList.remove("Peach");

// get selected value
// dataList.currentvalue;