import { Component } from '@angular/core';
import { TopBarComponent } from '../top-bar/top-bar.component';

@Component({
  selector: 'app-music-catalogue',
  standalone: true,
  imports: [TopBarComponent],
  templateUrl: './music-catalogue.component.html',
  styleUrl: './music-catalogue.component.css'
})
export class MusicCatalogueComponent {

}
