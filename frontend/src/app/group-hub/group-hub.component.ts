import { Component } from '@angular/core';
import { TranslateModule } from '@ngx-translate/core';
import { Router } from '@angular/router';
import { TopBarComponent } from '../bars/top-bar.component';
import { SideBarComponent } from '../bars/side-bar.component';

@Component({
  selector: 'app-group-hub',
  standalone: true,
  imports: [TranslateModule, TopBarComponent, SideBarComponent],
  templateUrl: './group-hub.component.html',
  styleUrl: './group-hub.component.css'
})
export class GroupHubComponent {
  isAdmin = true
  group: any

  constructor(private router: Router) {
    this.group = history.state.group;
  }

  navigate(path: string) {
    let group = this.group
    this.router.navigate([this.router.url, path], {state: {group} } )
  }
}
