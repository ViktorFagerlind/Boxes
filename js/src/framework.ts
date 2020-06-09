'use strict'
export module Framework {
    
    export function div(classSelector?: string) : HTMLElement
    {
      let elem = document.createElement("div");
      if (classSelector)
      {
        elem.setAttribute("class", classSelector);
      }
    
      return elem;
    }

}
