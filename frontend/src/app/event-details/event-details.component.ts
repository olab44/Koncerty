import { Component } from '@angular/core';
import { TranslateModule } from '@ngx-translate/core';
import { TopBarComponent } from '../bars/top-bar.component';
import { SideBarComponent } from '../bars/side-bar.component';

@Component({
  selector: 'app-event-details',
  standalone: true,
  imports: [TranslateModule, TopBarComponent, SideBarComponent],
  templateUrl: './event-details.component.html',
  styleUrl: './event-details.component.css'
})
export class EventDetailsComponent {
  group: any
  event: any

  constructor() {
    this.group = history.state.group;
    this.event = history.state.event;
  }
}
