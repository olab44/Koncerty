import { Component } from '@angular/core';
import { TranslateModule } from '@ngx-translate/core';
import { Router } from '@angular/router';
import { TopBarComponent } from '../bars/top-bar.component';
import { SideBarComponent } from '../bars/side-bar.component';
import { GroupInfo } from '../interfaces';

@Component({
  selector: 'app-group-hub',
  standalone: true,
  imports: [TranslateModule, TopBarComponent, SideBarComponent],
  templateUrl: './group-hub.component.html',
  styleUrl: './group-hub.component.css'
})
export class GroupHubComponent {
  group: GroupInfo

  constructor(private router: Router) {
    this.group = history.state.group;
    console.log(this.group)
  }

  navigate(path: string) {
    const group = this.group
    this.router.navigate(["/group", path], {state: {group} } )
  }
}
