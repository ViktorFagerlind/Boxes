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

    export function addClass(elem: HTMLElement, className: string) : void {
      elem.classList.add(className);
    }

    export function removeClass(elem: HTMLElement, className: string) : void {
      elem.classList.remove(className);
    }
}
