import { Component, EventEmitter, Output } from '@angular/core';
import { TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-overlay-new-event',
  standalone: true,
  imports: [TranslateModule],
  templateUrl: './overlay-new-event.component.html',
  styleUrl: './overlay-new-event.component.css'
})
export class OverlayNewEventComponent {
  @Output() close = new EventEmitter<void>()

  closeOverlay() {
    this.close.emit()
  }
}
