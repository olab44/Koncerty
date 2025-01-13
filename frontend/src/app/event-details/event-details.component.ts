import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { TopBarComponent } from '../bars/top-bar/top-bar.component';
import { SideBarEventComponent } from '../bars/side-bar-event/side-bar-event.component';
import { GroupInfo} from '../interfaces';
import { SessionStateService } from '../services/session-state/session-state.service';

@Component({
  selector: 'app-event-details',
  standalone: true,
  imports: [CommonModule, TranslateModule, TopBarComponent, SideBarEventComponent],
  templateUrl: './event-details.component.html',
  styleUrl: './event-details.component.css'
})
export class EventDetailsComponent {
  group!: GroupInfo
  event: any

  constructor(private state: SessionStateService) {
    this.state.currentGroup.subscribe((group) => {
      this.group = group;
    });
    this.state.currentEvent.subscribe((event) => {
      this.event = event;
    });
  }
}
