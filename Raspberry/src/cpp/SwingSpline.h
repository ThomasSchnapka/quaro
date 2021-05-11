#ifndef SWINGSPLINE_H
#define SWINGSPLINE_H

namespace quaro {
    class SwingSpline {
        public:
            SwingSpline();
            ~SwingSpline();
            int get_leg_position(float t); 
            void change_spline(int to_be_changed, int liftoff_pos, int t);
    };
}

#endif
