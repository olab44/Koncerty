import { Component } from '@angular/core';
import { TopBarComponent } from '../bars/top-bar.component';
import { SideBarComponent } from '../bars/side-bar.component';

@Component({
  selector: 'app-group-hub',
  standalone: true,
  imports: [TopBarComponent, SideBarComponent],
  templateUrl: './group-hub.component.html',
  styleUrl: './group-hub.component.css'
})
export class GroupHubComponent {
  isAdmin = true

  gotoCatalogue() {}
  gotoCalendar() {}
  gotoForum() {}
  gotoControl() {}
}
