'use strict'
import { Framework } from './framework';

export module UIComponents
{

    interface IRenderable {
        render: (element: HTMLElement) => void;
    }

    export class Sidebar implements IRenderable {

        private sidebar: HTMLElement;

        private menus: SidebarMenu[];

        constructor() {
            this.sidebar = Framework.div("sidebar");
            this.menus = [
                new SidebarMenu("Graphs"),
                new SidebarMenu("Data"),
                new SidebarMenu("Funcs")
            ];
        }

        public render(parent: HTMLElement)
        {
            this.menus.forEach(menu => menu.render(this.sidebar));
            parent.append(this.sidebar);
        }
    }

    export class SidebarMenu implements IRenderable {

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