'use strict'
import { Framework } from './framework';

export module UIComponents
{

    interface IRenderable {
        render: (element: HTMLElement) => void;
    }

    export class SideBar implements IRenderable {

        private sidebar: HTMLElement;

        private menus: SideBarMenu[];

        constructor() {
            this.sidebar = Framework.div("sidebar");
            this.menus = [
                new SideBarMenu("Graphs"),
                new SideBarMenu("Data"),
                new SideBarMenu("Funcs")
            ];
        }

        public render(parent: HTMLElement)
        {
            this.menus.forEach(menu => menu.render(this.sidebar));
            parent.append(this.sidebar);
        }
    }

    export class SideBarMenu implements IRenderable {

        menu: HTMLElement;
        
        constructor(displayName: string) {
            this.menu = Framework.div("sidebar-menu");
            this.menu.innerText = displayName;

            hover(this.menu, () => {
                    Framework.addClass(this.menu, "sidebar-menu-hover");
                },
                () => {
                    Framework.removeClass(this.menu, "sidebar-menu-hover");
                });
        }

        render(parent: HTMLElement) {
            parent.append(this.menu);
        }
    }

    function hover(element: HTMLElement, onMouseOver: () => void, onMouseOut: () => void) {
        element.addEventListener("mouseover", onMouseOver);
        element.addEventListener("mouseout", onMouseOut);
    }
}