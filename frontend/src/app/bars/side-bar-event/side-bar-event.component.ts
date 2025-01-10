import { Component } from '@angular/core';
import { DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms'
import { TranslateModule } from '@ngx-translate/core';
import { SessionStateService } from '../../services/session-state/session-state.service';
import { EventInfo } from '../../interfaces';

@Component({
  selector: 'app-side-bar-event',
  standalone: true,
  imports: [FormsModule, TranslateModule, DatePipe],
  templateUrl: './side-bar-event.component.html',
  styleUrl: './side-bar-event.component.css'
})
export class SideBarEventComponent {
  event!: EventInfo
  editMessage = ""

  constructor(private state: SessionStateService) {
    this.state.currentEvent.subscribe((event) => {
      this.event = event;
    });
  }
}
