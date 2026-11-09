; Nspire Dev Expert System — production rules implemented in CLIPS.
; Facts are asserted by Python; exactly one recommendation is expected.
(deftemplate request
  (slot goal (allowed-symbols products company campaign))
  (slot payment (allowed-symbols yes no))
  (slot accounts (allowed-symbols yes no)))

(deftemplate recommendation
  (slot code)
  (slot rule-id))

(defrule R01-web-application
  (declare (salience 100))
  (request (accounts yes))
  (not (recommendation))
  =>
  (assert (recommendation (code web_app) (rule-id R01))))

(defrule R02-online-store
  (declare (salience 90))
  (request (goal products) (payment yes) (accounts no))
  (not (recommendation))
  =>
  (assert (recommendation (code online_store) (rule-id R02))))

(defrule R03-product-catalog
  (declare (salience 80))
  (request (goal products) (payment no) (accounts no))
  (not (recommendation))
  =>
  (assert (recommendation (code catalog) (rule-id R03))))

(defrule R04-corporate-site
  (declare (salience 70))
  (request (goal company) (accounts no))
  (not (recommendation))
  =>
  (assert (recommendation (code corporate) (rule-id R04))))

(defrule R05-landing-page
  (declare (salience 60))
  (request (goal campaign) (accounts no))
  (not (recommendation))
  =>
  (assert (recommendation (code landing) (rule-id R05))))
