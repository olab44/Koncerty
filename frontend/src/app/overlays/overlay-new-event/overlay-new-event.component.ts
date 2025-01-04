import { Component, EventEmitter, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { BackendService } from '../../services/backend-connection/backend.service';
import { EventCreate } from '../../interfaces';

@Component({
  selector: 'app-overlay-new-event',
  standalone: true,
  imports: [FormsModule, TranslateModule],
  templateUrl: './overlay-new-event.component.html',
  styleUrl: './overlay-new-event.component.css'
})
export class OverlayNewEventComponent {
  @Output() close = new EventEmitter<void>()

  constructor(
    private backend: BackendService,
  ) {}

  event: EventCreate = {
    name: '',
    description: '',
    date_start: '',
    date_end: '',
    location: '',
  }

  eventMessage: string = '...'

  validateDates(): boolean {
    if (!this.event.date_start || !this.event.date_end) { return false }
    const start = new Date(this.event.date_start);
    const end = new Date(this.event.date_end);
    if (end <= start) {
      this.eventMessage = "End date should come after the start date."
      return false
    }
    this.eventMessage = "..."
    return true
  }

  onSubmit() {
    this.backend.postRequest('', this.event)
    .subscribe({
        next: res => {
          this.eventMessage = "New event organised!"
          console.log(res)
        },
        error: e => {
          this.eventMessage = e.error.detail
          console.log(e)
        }
    })
  }

  closeOverlay() {
    this.close.emit()
  }
}
