import { Component, EventEmitter, Output } from '@angular/core';
import { TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-overlay-create-group',
  standalone: true,
  imports: [TranslateModule],
  templateUrl: './overlay-create-group.component.html',
  styleUrl: './overlay-create-group.component.css'
})
export class OverlayCreateGroupComponent {
  @Output() close = new EventEmitter<void>()

  createMessage = "..."

  createGroup(name: string, description: string): void {
    // TODO: API CALL
    this.createMessage = "<<create group status>>"
  }
  closeOverlay() {
    this.close.emit()
}
}
